# -*- coding: utf-8 -*-
# Zapier Code(Python) 단계용: accepted_class2031 메시지에서 한국인으로 보이는 이름을 모은다.
# WHY: 확인은 사람이 계약서·커먼앱으로 하므로 놓치지 않는 쪽(recall)을 우선한다 — Lee/Park 같은 겹치는 성씨도 수집.
import re

SURNAMES = set('''kim lee yi park pak choi choe jung jeong chung chong kang cho jo yoon yun jang chang lim im
han oh seo suh shin sin kwon hwang ahn an song hong yoo yu ko koh moon mun yang baek paik nam noh roh
ha jeon chun jun bae heo hur heu nah na byun byeon min jin chae jee ji woo wu son sohn ryu ryoo yeo
gu koo ku won hyun hyeon cha joo ju uhm um ham kweon gwon'''.split())

# 이름(given name) 음절 — 두 음절 이상이 전부 이 목록으로 쪼개지면 한국식 이름으로 본다
SYLLABLES = sorted(set('''ji min seo su soo hyun hyeon jae jun joon woo yeon eun ha hee jin young yeong won
sung seung hye ye yu da ah kyung sang dong tae hoon ho jeong jung hyuk hyo in na ri rin yoon yun bin
been chan chul gyu kyu mi mo mok nam ok seon sun sook suk wan wook yong yoo jee si sol so bo bum beom
dae do eon gun geun han hwan hwi il jong joo kwang ki gi myung nara rae sae seok song taek uk woong
yeol yul'''.split()), key=len, reverse=True)

HANGUL_SURNAMES = set('김이박최정강조윤장임한오서신권황안송홍유고문양백남노하전배허나변민진채지우손류여구원현차주엄함')

KOREA_CUES =re.compile(r'\b(korea|korean|seoul|busan|jeju|incheon|daegu|songdo|pangyo|bundang)\b|:kr:|🇰🇷', re.I)
CLIENT_TAG = re.compile(r'#client-([a-z-]+?)-\d{2}-\d{2}', re.I)
WORD = re.compile(r"[A-Za-z][A-Za-z'-]+")


def is_korean_given(token):
    t = token.lower().replace('-', '')
    def split(s):
        if not s:
            return 0
        for syl in SYLLABLES:
            if s.startswith(syl):
                n = split(s[len(syl):])
                if n is not None:
                    return n + 1
        return None
    n = split(t)
    return n is not None and n >= 2


def candidates(text):
    """한국인으로 보이는 이름 후보 목록(중복 제거, 등장 순)."""
    found = []
    # 1) 클라이언트 태그 안의 이름
    for m in CLIENT_TAG.finditer(text):
        parts = m.group(1).split('-')
        if any(p.lower() in SURNAMES for p in parts) or any(is_korean_given(p) for p in parts):
            found.append(' '.join(p.capitalize() for p in parts))
    # 2) 본문의 한글 이름
    found += [w for w in re.findall(r'[가-힣]{2,4}', text) if w[0] in HANGUL_SURNAMES]
    # 3) 본문의 영문 이름: 대문자로 시작하는 단어가 연달아 2~3개
    body = CLIENT_TAG.sub(' ', text)
    for m in re.finditer(r"\b([A-Z][a-z'-]+(?:\s+[A-Z][a-z'-]+){1,2})\b", body):
        words = m.group(1).split()
        if any(w.lower() in SURNAMES for w in words) or any(is_korean_given(w) for w in words):
            found.append(m.group(1))
    # 4) 한국 단서(korea/seoul/:kr: 등)가 있는데 이름을 못 찾았으면 메시지 자체를 후보로
    if not found and KOREA_CUES.search(text):
        found.append('(이름 미확인 — 한국 단서: ' + KOREA_CUES.search(text).group(0) + ')')
    seen, out = set(), []
    for f in found:
        if f.lower() not in seen:
            seen.add(f.lower())
            out.append(f)
    return out


# Zapier 진입점: input_data['text'] = Slack 메시지 본문
try:
    input_data  # noqa: F821
    names = candidates(input_data.get('text', ''))
    output = {'is_candidate': bool(names), 'names': ', '.join(names)}
except NameError:
    pass


if __name__ == '__main__':
    # 사용자 제공 실제 형식 — 한국인 없음
    for msg in [
        '#client-neha-binu-26-27 has an interview offer at Lancashire for Medicine <@U1> <@U2>',
        'Nesil Su Güvener has her first EU offer: Culinary Associate Degree, EHL - this course has 20 spaces only',
        'Transfer student #client-rania-afridi-26-27 from Illinois has her first acceptance to Depaul',
        'The wonderful #client-daisy-mcdaid-26-27 from California has her second - second already! - UK offer',
        'Yanimir Illiev from Bulgaria has his first offer from Criminology & Forensic Investigation from The University of Surrey.',
    ]:
        assert candidates(msg) == [], (msg, candidates(msg))
    # 한국인 예시
    assert candidates('#client-minjun-kim-26-27 has an offer from Stanford') == ['Minjun Kim']
    assert candidates('Seoyeon Park from Seoul got into Yale') == ['Seoyeon Park']
    assert candidates('Ji-woo Lee has her first offer') == ['Ji-woo Lee']
    assert candidates('#client-daniel-choi-26-27 has an offer') == ['Daniel Choi']
    assert candidates('Our student from Korea has an offer from NYU') == ['(이름 미확인 — 한국 단서: Korea)']
    assert candidates('김민준 학생 합격') == ['김민준']
    print('all checks passed')
