# Daily 발송 Zap 4단계 Code by Zapier (Python) — dbTodos에서 Daily 보고 생성
# WHY: Daily 페이지에 직접 쓰던 방식은 누락·휘발이 많아(ideate/2026-10-21-dbtodos-daily-integration.md)
#      dbTodos 하나만 쓰고 발송 시점에 오늘 Done = Completed, In progress = In Progress로 메시지를 만든다.
# Zapier 입력(Input Data):
#   notion_json = 3.5단계 Notion API Request 응답 본문(JSON 문자열)
#   today       = 2단계 Formatter 값(Asia/Seoul, YYYY-MM-DD로 시작)
#   leave_json  = Google Sheets API Request 응답 본문(Leave 2.0 `Raw Input` 탭 values, 없으면 휴가 표시 생략)
import json
import re

# 보고 순서·헤더·Leave 2.0 신청 이메일(Config 탭 email 열).
# 이름은 Notion Host 이름에 이 키가 들어 있으면 매칭(대소문자 무시)
MEMBERS = [
    ('Harry', '🧑', 'h.yun@crimsoneducation.org'),
    ('Richard', '👨', 'richard.kim@crimsoneducation.org'),
    ('Hanna', '🍁', 'n.han@crimsoneducation.org'),
]


def plain(rich):
    return ''.join(r.get('plain_text', '') for r in rich or [])


def collect(pages, today):
    """Host 이름 → {'done': [...], 'wip': [...]}"""
    out = {}
    for p in pages:
        props = p.get('properties', {})
        title = plain(props.get('Tasks', {}).get('title')).strip()
        status = (props.get('Status', {}).get('status') or {}).get('name')
        done = ((props.get('Done date', {}).get('date') or {}).get('start') or '')[:10]
        if not title:
            continue
        if status == 'Done' and done == today:
            kind = 'done'
        elif status == 'In progress':
            kind = 'wip'
        else:
            continue  # 지난주 Done(필터 범위)·다른 상태는 제외
        for person in props.get('Host', {}).get('people', []):
            out.setdefault(person.get('name') or '?', {'done': [], 'wip': []})[kind].append(title)
    return out


def mdy(s):
    """Raw Input 날짜 '10/22/2026' → '2026-10-22'"""
    m, d, y = s.strip().split('/')
    return f'{y}-{int(m):02d}-{int(d):02d}'


def hour(t):
    """'14:00' → '14', '10:30' → '10:30'"""
    return t[:-3] if t.endswith(':00') else t


def leaves(values, today):
    """이메일 → ['Day off' | '연차 14-18시', ...]. 승인된 '연차/대휴 사용'만 보고, 대휴 적립은 무시"""
    if not values:
        return {}
    head, out = values[0], {}
    for row in values[1:]:
        r = dict(zip(head, row + [''] * (len(head) - len(row))))
        if r.get('Request Type') != '연차/대휴 사용' or r.get('Status') != '승인':
            continue
        try:
            start = mdy(r['Start Date'])
            end = mdy(r['End Date'] or r['Start Date'])
        except (KeyError, ValueError):
            continue
        if not start <= today <= end:
            continue
        if r.get('Is Full Day') == '아니오' and r.get('Start Time'):
            label = f"{r['Leave Type']} {hour(r['Start Time'])}-{hour(r['End Time'])}시"
        else:
            label = 'Day off'
        out.setdefault(r.get('Email', '').strip().lower(), []).append(label)
    return out


def to_markdown(groups, off):
    blocks, used = [], set()
    for key, emoji, email in MEMBERS:
        names = [n for n in groups if key.lower() in n.lower()]
        used.update(names)
        items = {'done': [], 'wip': []}
        for n in names:
            items['done'] += groups[n]['done']
            items['wip'] += groups[n]['wip']
        blocks.append(section(f'{emoji} {key}', items, off.get(email, [])))
    for n in sorted(set(groups) - used):  # MEMBERS에 없는 Host도 빠뜨리지 않음
        blocks.append(section(n, groups[n]))
    return '\n\n'.join(blocks)


def section(header, items, labels=()):
    if 'Day off' in labels and not items['done'] and not items['wip']:
        return f'## {header}\n\nDay off'  # 기존 Daily 템플릿의 휴가 표기
    if labels:
        header += f" ({', '.join(labels)})"
    lines = [f'## {header}', '', '✅ Completed:']
    lines += [f'- {t}' for t in items['done']] or ['- 기록 없음']
    lines += ['', '🚧 In Progress:']
    lines += [f'- {t}' for t in items['wip']] or ['- 기록 없음']
    return '\n'.join(lines)


def to_slack(text):
    # 기존 4단계 변환 로직 그대로
    def heading_repl(m):
        content = m.group(1).strip()
        content = re.sub(r'^\*+\s*', '', content)
        content = re.sub(r'\s*\*+$', '', content)
        return f'*{content}*'
    text = re.sub(r'(?m)^#{1,6}\s*(.+)$', heading_repl, text)
    text = re.sub(r'\*\*\s*(.*?)\s*\*\*', r'*\1*', text)
    text = re.sub(r'(?m)^\s*-\s*$', '', text)
    text = re.sub(r'(?m)^\s*-\s+', '• ', text)
    text = re.sub(r'\[(.*?)\]\((https?://[^\s)]+)\)', r'<\2|\1>', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+(?=\n)', '', text)
    return text


def to_blocks(md):
    """Markdown → Notion blocks(children). 오늘 Daily 페이지(빈 템플릿)에 Notion API로 붙일 본문"""
    def block(kind, text, **extra):
        return {'object': 'block', 'type': kind,
                kind: {'rich_text': [{'type': 'text', 'text': {'content': text}}], **extra}}
    out = []
    for line in md.split('\n'):
        if line.startswith('## '):
            out.append(block('heading_2', line[3:], color='blue_background'))  # 기존 템플릿 팀원 헤더 색
        elif line.startswith('- '):
            out.append(block('bulleted_list_item', line[2:]))
        elif line.strip():
            out.append(block('paragraph', line))
    return out


def build(data):
    raw = data.get('notion_json') or '{}'
    if raw.startswith('http'):  # API Request의 Full Response Data는 Zapier 파일 링크로 넘어옴
        import requests
        raw = requests.get(raw).text
    body = json.loads(raw)
    today = (data.get('today') or '')[:10]
    off = leaves(json.loads(data.get('leave_json') or '{}').get('values', []), today)
    md = to_markdown(collect(body.get('results', []), today), off)
    return {'text': to_slack(md), 'markdown': md,
            'blocks_json': json.dumps({'children': to_blocks(md)}, ensure_ascii=False)}


if 'input_data' in globals():
    output = build(input_data)  # noqa: F821 — Zapier가 주입
else:
    def page(title, status, host, done=None):
        return {'properties': {
            'Tasks': {'title': [{'plain_text': title}]},
            'Status': {'status': {'name': status}},
            'Done date': {'date': {'start': done} if done else None},
            'Host': {'people': [{'name': host}]},
        }}
    sample = {'results': [
        page('오늘 끝낸 일', 'Done', 'Harry', '2026-10-22'),
        page('어제 끝낸 일', 'Done', 'Harry', '2026-10-21'),
        page('진행 중', 'In progress', 'Harry'),
        page('리처드 일', 'Done', 'Richard Kim', '2026-10-22'),
        page('제니 일', 'Done', 'Jennie', '2026-10-22'),
        page('아이디어', 'On-track_IDEA', 'Hanna'),
    ]}
    r = build({'notion_json': json.dumps(sample), 'today': '2026-10-22T19:00:00+0900'})
    md = r['markdown']
    assert '- 오늘 끝낸 일' in md and '어제 끝낸 일' not in md
    assert md.index('오늘 끝낸 일') < md.index('🚧') and '- 진행 중' in md
    assert '## 👨 Richard\n\n✅ Completed:\n- 리처드 일' in md   # 부분 이름 매칭
    assert '## 🍁 Hanna\n\n✅ Completed:\n- 기록 없음' in md    # IDEA 상태 제외
    assert '## Jennie' in md                                # MEMBERS 밖 Host도 표시
    assert r['text'].startswith('*🧑 Harry*') and '• 오늘 끝낸 일' in r['text']

    # 휴가: Raw Input 헤더 그대로, 짧은 행(뒤 빈칸 생략)도 처리
    head = ['Timestamp', 'Email', 'Request Type', 'Leave Type', 'Is Multi-day', 'Start Date', 'End Date',
            'Is Full Day', 'Start Time', 'End Time', 'Reason', 'Status']
    leave = {'values': [head,
        ['', 'n.han@crimsoneducation.org', '연차/대휴 사용', '연차', '예', '10/21/2026', '10/23/2026', '', '', '', '', '승인'],
        ['', 'richard.kim@crimsoneducation.org', '연차/대휴 사용', '대휴', '아니오', '10/22/2026', '10/22/2026', '아니오', '9:00', '10:30', '', '승인'],
        ['', 'h.yun@crimsoneducation.org', '대휴 적립', '', '', '10/22/2026', '10/22/2026', '', '6:00', '7:00', '', '승인'],
        ['', 'h.yun@crimsoneducation.org', '연차/대휴 사용', '연차', '아니오', '10/22/2026', '10/22/2026', '예', '', '', '', '반려'],
    ]}
    md = build({'notion_json': json.dumps(sample), 'today': '2026-10-22',
                'leave_json': json.dumps(leave)})['markdown']
    assert '## 🍁 Hanna\n\nDay off' in md                       # 여러 날 종일 휴가, 기록 없음
    assert '## 👨 Richard (대휴 9-10:30시)' in md                 # 시간 단위, 기록 있음
    assert '## 🧑 Harry\n' in md                                  # 대휴 적립·반려는 무시
    assert build({'notion_json': json.dumps(sample), 'today': '2026-10-22'})['markdown'].count('Day off') == 0

    # Daily 페이지 블록: 헤더·문단·불릿, 빈 줄은 건너뜀
    blocks = json.loads(build({'notion_json': json.dumps(sample), 'today': '2026-10-22'})['blocks_json'])['children']
    kinds = [b['type'] for b in blocks]
    assert kinds[:4] == ['heading_2', 'paragraph', 'bulleted_list_item', 'paragraph']
    assert blocks[0]['heading_2']['rich_text'][0]['text']['content'] == '🧑 Harry'
    assert blocks[2]['bulleted_list_item']['rich_text'][0]['text']['content'] == '오늘 끝낸 일'
    print('ok')
    print(r['text'])
