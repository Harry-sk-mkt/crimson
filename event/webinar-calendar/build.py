# -*- coding: utf-8 -*-
import sys, re, json; sys.stdout.reconfigure(encoding="utf-8")
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter
src_path, ev_path, out_path = sys.argv[1:4]

def clean(n):
    n = re.sub(r"^WB-\d{4}-\d{2}-KOR-MOFU[- ](Core |Rise )?", "", n)
    n = re.sub(r"\s*\((\d+/\d+|PM|AM|Recording)\)", "", n)
    n = re.sub(r"^Recording ", "", n)
    return n.strip()

# 실적 출처: lead-tracker Events_OPS 웨비나 행(Revenue = Deal Tracker 기준), 2026-10-16 덤프(TEMPQA_075)
kr = []
with open(ev_path, encoding="utf-8") as f:
    next(f)
    for line in f:
        lsd, n, d, rv = line.rstrip("\n").split("\t")
        if "BOFU" in lsd or "MOFU-CGA" in lsd or re.search(r" (SG|VN|HK|EXP|LG)$|joining|in USA|in ID", lsd): continue
        kr.append(dict(name=lsd, title=clean(lsd), nlp1=int(n), deals=int(d), rev=float(rv)))

# 같은 주제가 회차마다 이름이 조금씩 다른 경우
ALIASES = {
 "Competitions Recognised By Colleges and Majors": ["Competitions Recognized by Colleges"],
 "Admissions Process Simulation with Josephine Lee": ["Admission Process Simulation"],
 "Game changing Common Application Tips": ["Game Changing Common Application Tips & Case Studies", "Game changing Common Application Tips and Case Studies"],
 "EA/ED Application Strategy": ["EA/ED Strategy"],
 "College Research 1: HYPSM + Ivy by MIT FAO": ["College Research: HYPS & Ivy"],
 "College Research 2: US Top 15 - 30 + NYU": ["College Research: Top 20-30"],
 "Grades vs. ECs": ["Grades vs ECs"],
 "Successful Korean Common App Showcases": ["RISE: Successful Korean Common App Showcases"],
 "How to Get Into Top Selective Summer Programs": ["Top Summer Programs"],
}

def best(title):
    names = [title] + ALIASES.get(title, [])
    runs = [o for o in kr if o["title"] in names]
    assert runs, "no run: " + title
    return max(runs, key=lambda o: (o["nlp1"], o["rev"]))

def P(title, label=None):
    b = best(title); n = b["nlp1"]
    mark = "★" if (n >= 15 or b["rev"] >= 100000) else "·"
    return f"{mark} {label or title} (NLP1 {n}·${b['rev']/1000:,.0f}k)"

def N(title):  # FY27 plan topic, no KR run yet
    return f"◇ {title} (FY27 계획·신규)"

G = {
"Grade 8": [
 [P("Start Building Winning Profiles From GR 7 to 9"), P("EC for Each Year of High School")],
 [P("How to Get Into Top Selective Summer Programs"), P("RISE Academic & EC Planning")],
 [P("Extracurricular Strategy for Young Students"), P("Admission Programs for Young Students")],
 [P("How To Maximize Your Winter Break")],
 [P("Rise Webinar for G6~8 Young Students"), P("Competitions Recognised By Colleges and Majors")],
 [P("How to Ace Your Curriculum")],
 [P("All about AP & IB curriculum"), N("IB vs AP vs A-Level for Middle Schoolers")],
 [P("AP vs IB Course Selection"), N("RISE Summer Planning")],
 [P("RISE What Middle Schooler Should Do In Summer")],
 [N("RISE Summer Project Planning")],
 [N("RISE Long-term Profile Building")],
 [P("Rise Stanford Roadmap for rising G8~9"), N("RISE Transition to High School")],
],
"Grade 9": [
 [P("EC for Each Year of High School"), P("Start Building Winning Profiles From GR 7 to 9")],
 [P("How to Get Into Top Selective Summer Programs")],
 [P("SAT One Day Class")],
 [P("Extracurricular Strategy for Young Students"), P("How To Maximize Your Winter Break")],
 [P("Grades vs. ECs")],
 [P("How to Recover from Bad Grades and Still Get Into Top Colleges"), P("Competitions Recognised By Colleges and Majors")],
 [P("AP vs IB Course Selection"), P("All about AP & IB curriculum")],
 [P("Maximizing Extracurricular in Your Summer Break")],
 [P("What You Must Do Other Than Summer Programs")],
 [P("ECs and Competition Evaluation with FAO")],
 [P("SAT One-day Class")],
 [P("Before Back to School"), N("Back-to-School Profile Planning")],
],
"Grade 10": [
 [P("US/UK Major Selection"), P("EC for Each Year of High School")],
 [P("How to Get Into Top Selective Summer Programs")],
 [P("Major Strategy Webinar Part 2: Humanity & Liberal Arts"), P("Major Strategy Webinar Part 1: Natural Sciences & Engineering & STEM")],
 [P("Extracurricular and Leadership Projects Showcase"), P("Competitions Recognised By Colleges and Majors")],
 [P("SAT One Day Class"), P("How To Maximize Your Winter Break")],
 [P("Grades vs. ECs")],
 [P("AP vs IB Course Selection"), P("How to Ace Your Curriculum")],
 [P("Maximizing Extracurricular in Your Summer Break")],
 [P("What You Must Do Other Than Summer Programs")],
 [P("All about AP & IB curriculum")],
 [P("ECs and Competition Evaluation with FAO")],
 [P("Admission Roadmap for Sophomores & Juniors")],
],
"Grade 11": [
 [P("Admission Roadmap for Sophomores & Juniors"), P("The Difference Between a Stanford and Harvard Admit")],
 [P("Admissions Process Simulation with Josephine Lee", "Admission Process Simulation")],
 [P("College Research 2: US Top 15 - 30 + NYU"), P("College Research 1: HYPSM + Ivy by MIT FAO"), P("SAT One Day Class")],
 [P("How to Get into California Universities?"), P("Ivy Admit Rate Secret")],
 [P("2024 EA Result Analysis", "EA Result Analysis"), P("How to Recover from Bad Grades and Still Get Into Top Colleges")],
 [P("2026 Admissions Trends", "Admissions Trends")],
 [P("Common App Review - What FAO Liked"), P("Successful Korean Common App Showcases")],
 [P("Application Tips and Timeline for 2026 Applicants", "Application Tips and Timeline for Next-Year Applicants")],
 [P("Accepted Student Panel Webinar")],
 [P("Admissions Trends With EA/ED and RD Results"), P("Online Essay Workshop")],
 [P("Common app Package for Rising 12 & Essay"), P("Where's My School Fit?")],
 [P("Where's My School Fit"), P("Building an Honors Strategy for US Application"), P("California Dream: A Comprehensive Guide to the UC System")],
],
"Grade 12": [
 [P("EA/ED Application Strategy"), P("Game changing Common Application Tips")],
 [P("How to Get into California Universities?"), P("Common App Review - What Impressed AOs")],
 [P("How to Write the Perfect Personal Statement"), P("EA/ED Application Strategy")],
 [P("How to build an outstanding Common App")],
 [P("2024 EA Result Analysis", "EA Result Analysis"), P("Plan Your Application Now")],
 [P("2025 EA Result Analysis And CGA EAED", "EA/ED Result Analysis")],
 [], [N("RD Waitlist Guide")], [], [P("Transfer & Gap Year")], [], [],
],
}
MONTHS = ["August","September","October","November","December","January","February","March","April","May","June","July"]
M = {m[:3]: i for i, m in enumerate(MONTHS)}

# 2026-10-16 사용자 결정: 학사일정과 같은 달에 넣은 주제는 경쟁사보다 늦어 보이므로 1달 앞당겨 선점.
# (grade, 원래 달, 주제 일부, 대비하는 일정) — 2달+ 선행 / 결과분석(사후) / 날짜 무관 주제는 그대로.
MOVES = [
 ("Grade 8", "Sep", "Top Selective Summer", "9월 썸머 프로그램 선정"),
 ("Grade 8", "Dec", "Rise Webinar for G6~8", "12월 겨울방학"),
 ("Grade 8", "Dec", "Competitions Recognised", "12월 겨울방학"),
 ("Grade 8", "Jan", "Ace Your Curriculum", "1월 2학기"),
 ("Grade 8", "Mar", "AP vs IB Course Selection", "3월 수강신청"),
 ("Grade 9", "Sep", "Top Selective Summer", "9월 썸머 프로그램 선정"),
 ("Grade 9", "Oct", "SAT One Day Class", "10월 PSAT"),
 ("Grade 9", "Dec", "Grades vs. ECs", "12월 1학기 종료"),
 ("Grade 9", "Jan", "Recover from Bad Grades", "1월 성적·2학기"),
 ("Grade 9", "Jun", "SAT One-day Class", "6월 방학 SAT 집중"),
 ("Grade 10", "Sep", "Top Selective Summer", "9월 썸머 프로그램 선정"),
 ("Grade 10", "Dec", "Maximize Your Winter Break", "12월 겨울방학"),
 ("Grade 10", "Jan", "Grades vs. ECs", "1월 2학기"),
 ("Grade 10", "May", "All about AP & IB", "5월 AP 시험·IB HL/SL 결정"),
 ("Grade 10", "Jun", "ECs and Competition Evaluation", "6월 여름방학"),
 ("Grade 11", "Nov", "California Universities", "11월 대학 리스트"),
 ("Grade 11", "Nov", "Ivy Admit Rate Secret", "11월 대학 리스트"),
 ("Grade 11", "Jul", "School Fit (NLP1", "7월 대학 리스트 확정"),
 ("Grade 11", "Jul", "Honors Strategy", "7월 대학 리스트 확정"),
 ("Grade 12", "Aug", "Game changing Common Application", "8월 Common App 오픈"),
 ("Grade 12", "Nov", "outstanding Common App", "11월 UC 마감"),
 ("Grade 12", "May", "Transfer & Gap Year", "5/1 등록 결정"),
]
for g, frm, key, why in MOVES:
    cells = G[g]; i = M[frm]
    hit = [t for t in cells[i] if key in t]
    assert len(hit) == 1, (g, frm, key, hit)
    cells[i].remove(hit[0])
    core = lambda t: t[2:].split(" (")[0].rstrip("?")  # 앞의 ★/·/◇ 표시 제외
    # 8월(새 학년 시작)의 1달 전은 같은 학년 7월이 아니라 직전 학년의 7월
    target = cells[i - 1] if i > 0 else G[list(G)[list(G).index(g) - 1]][11]
    if any(core(t) == core(hit[0]) for t in target): continue  # 앞 달에 이미 같은 주제 → 중복 없이 제거만
    target.append(hit[0] + f" ⇢ {why} 대비")

# ---------------------------------------------------------------
# 2026-10-16 사용자 결정: 소재 단에서 비슷하게 인지되는 주제(학년 무관)는 두 달 연속 금지.
# 분류는 사용자가 정한 14개. 겹치면 "1달 전 원칙에 맞는 달"에 모은다.
# 주제 → 분류 매핑은 Claude가 붙인 것(사용자 검토 대상) — 위에서부터 첫 매칭.
CATS = [
 ("결과분석·트렌드", ["Result Analysis", "Admissions Trends", "Waitlist"]),
 ("EA/ED 전략", ["EA/ED Application Strategy", "Plan Your Application"]),
 ("여름방학", ["Summer"]),
 ("겨울방학", ["Winter Break"]),
 ("대회", ["Competition"]),
 ("성적·학업", ["Grades", "Ace Your Curriculum"]),
 ("AP·IB", ["AP & IB", "AP vs IB", "A-Level"]),
 ("SAT", ["SAT"]),
 ("전공", ["Major"]),
 ("리서치", ["College Research", "California", "Ivy Admit", "School Fit"]),
 # 2026-10-19 사용자: "Common App Review"는 커먼앱이 아니라 Success Profile Review by FAO → 프로필. 첫 매칭이라 커먼앱보다 위에 둔다.
 ("프로필(케이스 스터디)", ["Stanford and Harvard Admit", "Leadership Projects Showcase", "Accepted Student", "Common App Review"]),
 ("커먼앱", ["Common App"]),
 ("에세이", ["Personal Statement", "Essay Workshop"]),
 # 2026-10-19 사용자: Before Back to School은 "신학기 준비" 얘기라 로드맵과 다름.
 ("신학기 준비", ["Before Back to School"]),
 ("로드맵", ["Roadmap", "EC for Each Year", "Winning Profiles", "Transition to High School", "Profile Planning",
          "Profile Building", "Academic & EC Planning", "Application Tips and Timeline", "Young Students",
          "Rise Webinar for G6~8"]),
]
def cat(t):
    for name, kws in CATS:
        if any(k.lower() in t.lower() for k in kws):
            # 2026-10-19 사용자: RISE는 중학생 타겟이라 같은 분류의 고학년 주제와 붙어도 됨 → 분류를 따로 센다(RISE끼리는 연속 금지 유지)
            return name + "·RISE" if re.match(r"\S+ rise\b", t.lower()) else name
    return None  # Simulation / Honors / Transfer — 분류 밖, 연속 규칙 미적용

# 원래 배치 중 이미 "학사일정 1달 전"에 맞던 주제 (+ ⇢ 표시로 앞당긴 주제)
ALIGNED = {
 ("Grade 8", "Nov", "Winter Break"), ("Grade 8", "Feb", "AP & IB"), ("Grade 8", "Feb", "A-Level"),
 ("Grade 8", "May", "Summer Project"), ("Grade 8", "Jul", "Stanford Roadmap"), ("Grade 8", "Jul", "Transition"),
 ("Grade 9", "Nov", "Winter Break"), ("Grade 9", "Feb", "AP vs IB"), ("Grade 9", "Feb", "AP & IB"),
 ("Grade 9", "May", "Competition Evaluation"), ("Grade 9", "Jul", "Back to School"), ("Grade 9", "Jul", "Profile Planning"),
 ("Grade 10", "Feb", "AP vs IB"), ("Grade 10", "Feb", "Ace Your Curriculum"), ("Grade 10", "Jul", "Sophomores"),
 ("Grade 11", "Oct", "College Research"), ("Grade 11", "Jan", "Admissions Trends"), ("Grade 11", "Jul", "California Dream"),
 ("Grade 12", "Oct", "EA/ED Application Strategy"), ("Grade 12", "Oct", "Personal Statement"),
 ("Grade 12", "Dec", "Plan Your Application"), ("Grade 12", "Mar", "Waitlist"),
}
def aligned(g, j, t):
    return "⇢" in t or any(g == ag and MONTHS[j][:3] == am and k in t for ag, am, k in ALIGNED)
def nlp1(t):
    m = re.search(r"NLP1 (\d+)", t); return int(m.group(1)) if m else 0

GRADES = list(G)
CONSEC_LOG = []
CAT_NAMES = [c for c, _ in CATS] + [c + "·RISE" for c, _ in CATS]  # cat()이 RISE 주제를 '분류·RISE'로 따로 셈
# 2026-10-19 사용자: 프로필(케이스 스터디)은 아무 달이나 가능 + 연속 금지 미적용
CONSEC_EXEMPT = {"프로필(케이스 스터디)", "프로필(케이스 스터디)·RISE"}
for cname in [c for c in CAT_NAMES if c not in CONSEC_EXEMPT]:
    months = sorted({j for g in G for j in range(12) for t in G[g][j] if cat(t) == cname})
    if len(months) < 2: continue
    # 원형(7월→8월 연결) 연속 구간 나누기
    ms = set(months); runs = []; seen = set()
    for j in months:
        if j in seen or ((j - 1) % 12) in ms and len(ms) < 12: continue
        run = [];  k = j
        while k in ms and k not in seen: run.append(k); seen.add(k); k = (k + 1) % 12
        runs.append(run)
    for run in runs:
        if len(run) < 2: continue
        items = {j: [(g, t) for g in G for t in G[g][j] if cat(t) == cname] for j in run}
        score = lambda j: (sum(aligned(g, j, t) for g, t in items[j]), max(nlp1(t) for _, t in items[j]))
        cands = [j for j in run if score(j)[0] > 0] or [max(run, key=lambda j: score(j)[1])]
        anchors = []
        for j in sorted(cands, key=score, reverse=True):
            if all(abs(run.index(j) - run.index(a)) > 1 for a in anchors): anchors.append(j)
        for j in run:
            if j in anchors: continue
            dest = min(anchors, key=lambda a: (abs(run.index(j) - run.index(a)), -score(a)[0]))
            for g, t in items[j]:
                G[g][j].remove(t)
                gi = GRADES.index(g)
                # 월이 학년 경계(7월↔8월)를 넘으면 행도 옮김 (G8 8월→7월은 프레임 밖이라 같은 행 유지)
                if j == 0 and dest == 11 and gi > 0: g2 = GRADES[gi - 1]
                elif j == 11 and dest == 0 and gi < len(GRADES) - 1: g2 = GRADES[gi + 1]
                else: g2 = g
                core2 = lambda x: x[2:].split(" (")[0].rstrip("?")
                if any(core2(x) == core2(t) for x in G[g2][dest]):
                    CONSEC_LOG.append(f"[{cname}] {g} {MONTHS[j][:3]} → 중복이라 제거: {t[:60]}")
                    continue
                G[g2][dest].append(t + f" ⇄ {MONTHS[j][:3]}→{MONTHS[dest][:3]} 연속 회피")
                CONSEC_LOG.append(f"[{cname}] {g} {MONTHS[j][:3]} → {g2} {MONTHS[dest][:3]}: {t[:60]}")
print("\n".join(CONSEC_LOG))

# ---------------------------------------------------------------
# 2026-10-19 사용자 결정: 웨비나는 주 1회(수요일 라이브) → 월 상한 = 그 달 수요일 수.
# 같은 주제가 여러 학년 칸에 있어도 웨비나 1회로 센다. 상한을 넘는 달은 우선순위 낮은 주제부터
# 앞 달로(1달 전 선점 원칙 유지), 안 되면(앞당긴 주제가 아닐 때만) 다음 달로, 그래도 안 되면 "대기 후보" 탭으로.
# 우선순위: ★ > 학사일정 1달 전에 맞는 주제 > ◇(FY27 계획) > · , 같으면 NLP1.
# (1달 전 우선으로 했더니 EC for Each Year(NLP1 58)가 빠지고 미검증 ◇가 남아서 ★를 맨 앞으로)
import calendar
FY_START = 2026  # FY27 = 2026-08 ~ 2027-07 기준 수요일 수
CAP = [sum(1 for d, wd in calendar.Calendar().itermonthdays2(FY_START + (j >= 5), (j + 7) % 12 + 1) if d and wd == 2)
       for j in range(12)]
core = lambda t: t[2:].split(" (")[0].rstrip("?")
def webinars(j):
    out = {}
    for g in G:
        for t in G[g][j]: out.setdefault(core(t), []).append((g, t))
    return out
def rank(j, items):
    ts = [t for _, t in items]
    return (any(t[0] == "★" for t in ts), any(aligned(g, j, t) for g, t in items),
            any(t[0] == "◇" for t in ts), max(nlp1(t) for t in ts))
def row_for(g, j, dest):  # 7월↔8월 학년 경계를 넘으면 행도 옮김 (위 연속 회피와 같은 규칙)
    gi = GRADES.index(g)
    if j == 0 and dest == 11 and gi > 0: return GRADES[gi - 1]
    if j == 11 and dest == 0 and gi < len(GRADES) - 1: return GRADES[gi + 1]
    return g
def cat_ok(c, j, key, dest):
    if c is None: return True
    ms = {m for g in G for m in range(12) for t in G[g][m] if cat(t) == c and not (m == j and core(t) == key)} | {dest}
    return not any((m + 1) % 12 in ms for m in ms)
WAITLIST, CAP_LOG = [], []
for j in reversed(range(12)):  # 7월부터 거꾸로 — 앞 달로 미는 방향이라 밀려온 주제가 다시 넘치지 않게
    ws_ = webinars(j)
    for key in sorted(ws_, key=lambda k: rank(j, ws_[k]))[:max(0, len(ws_) - CAP[j])]:
        items = ws_[key]; c = cat(items[0][1])
        dests = [(j - 1) % 12] + ([] if rank(j, items)[1] else [(j + 1) % 12])
        for dest in dests:
            if (key in webinars(dest) or len(webinars(dest)) < CAP[dest]) and cat_ok(c, j, key, dest):
                for g, t in items:
                    G[g][j].remove(t); g2 = row_for(g, j, dest)
                    if not any(core(x) == key for x in G[g2][dest]):
                        G[g2][dest].append(t + f" ⇠ {MONTHS[j][:3]}→{MONTHS[dest][:3]} 월 상한")
                CAP_LOG.append(f"[상한] {MONTHS[j][:3]} → {MONTHS[dest][:3]}: {key}")
                break
        else:
            for g, t in items:
                G[g][j].remove(t); WAITLIST.append((g, j, t))
            CAP_LOG.append(f"[후보] {MONTHS[j][:3]}: {key}")
print("\n".join(CAP_LOG))
# 검증: 모든 달이 상한 이하
for j in range(12): assert len(webinars(j)) <= CAP[j], (MONTHS[j], len(webinars(j)), CAP[j])
# 검증: 어떤 분류도 두 달 연속(7월→8월 포함)으로 나오지 않아야 함 (CONSEC_EXEMPT 제외)
for cname in [c for c in CAT_NAMES if c not in CONSEC_EXEMPT]:
    ms = {j for g in G for j in range(12) for t in G[g][j] if cat(t) == cname}
    bad = [MONTHS[j][:3] for j in ms if (j + 1) % 12 in ms]
    assert not bad, (cname, bad)
print("UNCATEGORIZED:", sorted({t[2:40] for g in G for c in G[g] for t in c if cat(t) is None}))

wb = openpyxl.Workbook()
ws = wb.active; ws.title = "웨비나 캘린더"
src = openpyxl.load_workbook(src_path, data_only=True)["TimelineG8-12"]
thin = Side(style="thin", color="BFBFBF"); box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
grey = Font(italic=True, color="595959")

ws["A1"] = "Grade 8 to 12 Monthly Webinar Calendar"; ws["A1"].font = Font(bold=True, size=14)
ws["A2"] = "범례: ★ 검증된 주제(New P1 15+ 또는 Revenue $100k+)  /  $000k = 그 회차 Revenue(Events_OPS, Deal Tracker 기준)  · 진행했지만 실적 보통  ◇ FY27 계획에만 있고 아직 안 한 주제  /  괄호 = 과거 회차 중 가장 좋은 회차 실적  /  각 칸 메모 = 원본 타임라인 내용  /  배치 원칙: 학사일정 1달 전 웨비나로 선점(⇢ = 다음 달 일정 대비로 앞당긴 주제), 결과분석은 발표 직후  /  같은 분류(주제 분류 탭)는 학년 무관 두 달 연속 금지(⇄ = 연속 회피로 옮긴 주제)  /  월 상한 = 그 달 수요일 수(주 1회, FY27 기준), 같은 주제는 학년이 여러 개여도 1회(⇠ = 상한 때문에 옮긴 주제, 못 옮긴 주제는 '대기 후보' 탭)"
ws["A2"].font = grey
for r_src, label in [(3, "입시 일정"), (4, "학사·휴일")]:
    ws.cell(r_src, 1, label).font = Font(bold=True)
    for c in range(2, 14):
        v = src.cell(r_src, c).value
        if v: ws.cell(r_src, c, v).alignment = wrap
psat = src.cell(2, 13).value
if psat:
    cur = ws.cell(3, 13).value
    ws.cell(3, 13, (str(cur) + "\n" if cur else "") + str(psat).strip()).alignment = wrap

fill = PatternFill("solid", fgColor="1F3864")
for i, h in enumerate(["Grade"] + MONTHS, 1):
    c = ws.cell(5, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = fill
    c.alignment = Alignment(horizontal="center", vertical="center"); c.border = box

for i, (g, cells) in enumerate(G.items()):
    r = 6 + i
    a = ws.cell(r, 1, src.cell(r, 1).value or g); a.font = Font(bold=True); a.alignment = wrap; a.border = box
    for j, topics in enumerate(cells):
        c = ws.cell(r, 2 + j, "\n".join(topics))
        c.alignment = wrap; c.border = box
        tl = src.cell(r, 2 + j).value
        if tl: c.comment = Comment("타임라인: " + str(tl)[:900], "Claude", width=320, height=220)
ws.cell(11, 1, "월 웨비나 수 / 상한").font = Font(bold=True)
for j in range(12):
    c = ws.cell(11, 2 + j, f"{len(webinars(j))} / {CAP[j]}"); c.alignment = Alignment(horizontal="center"); c.border = box

ws["A12"] = "G12 2~7월: 지원이 끝난 시기라 G12 대상 웨비나는 효과가 낮음 — 결과분석 웨비나는 G10~11 대상으로 활용"; ws["A12"].font = grey
ws["A13"] = "Source: 12 Month Marketing Execution Plan SK.xlsx — TimelineG8-12(학년별 타임라인), Events_OPS(웨비나 실적: SF NLP1s·Revenue, 2026-10-16 기준), FY27(계획 주제). 2026-10-16 정리, 10-19 월 상한 반영. 주제 배치는 Claude 초안 — 검토 필요"; ws["A13"].font = grey
ws.column_dimensions["A"].width = 16
for c in range(2, 14): ws.column_dimensions[get_column_letter(c)].width = 30
ws.row_dimensions[3].height = 30; ws.row_dimensions[4].height = 45
for r in range(6, 11): ws.row_dimensions[r].height = 120
ws.freeze_panes = "B6"

t = wb.create_sheet("학년별 타임라인(원본)")
for row in src.iter_rows(min_row=1, max_row=10, max_col=13):
    for c in row:
        if c.value is not None:
            t.cell(c.row, c.column, c.value).alignment = wrap
t["A1"].comment = Comment("Source: 12 Month Marketing Execution Plan SK.xlsx, TimelineG8-12 탭(값 복사), 2026-10-16", "Claude")
t.column_dimensions["A"].width = 16
for c in range(2, 14): t.column_dimensions[get_column_letter(c)].width = 34
for r in range(6, 11): t.row_dimensions[r].height = 200
t.freeze_panes = "B6"

d = wb.create_sheet("근거_웨비나 실적")
heads = ["Lead Source Detail", "Topic", "SF NLP1s", "#Deals", "Revenue"]
for i, h in enumerate(heads, 1):
    c = d.cell(1, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = fill
d["A1"].comment = Comment("Source: lead-tracker Events_OPS (EventType=Webinar, #Deals·Revenue는 Deal Tracker 기준), 298 rows, run 2026-10-16 16:27 KST. TEMPQA_075 runDumpEventsOPSWebinarRevenue() 로그를 사용자가 붙여넣음. 해외 공동(SG/VN/HK/TH/ID)·BOFU·CGA 제외.", "Claude", width=320, height=120)
rows = kr  # Events_OPS 시트 순서(대체로 최신순) 유지
for r, o in enumerate(rows, 2):
    for c, v in enumerate([o["name"], o["title"], o["nlp1"], o["deals"], round(o["rev"])], 1):
        d.cell(r, c, v)
d.column_dimensions["A"].width = 70; d.column_dimensions["B"].width = 55
d.freeze_panes = "A2"; d.auto_filter.ref = f"A1:E{len(rows)+1}"
for rr in range(2, len(rows) + 2): d.cell(rr, 5).number_format = '"$"#,##0'
k = wb.create_sheet("주제 분류")
for i, h in enumerate(["분류", "주제", "배치(학년·월)"], 1):
    c = k.cell(1, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = fill
k["A1"].comment = Comment("분류 14개는 사용자 지정(2026-10-16). 주제→분류 매핑은 Claude 초안 — 잘못 묶인 게 있으면 알려주세요. '분류 밖'은 연속 규칙 미적용.", "Claude", width=320, height=100)
places = {}
for g in G:
    for j in range(12):
        for t in G[g][j]:
            name = t[2:].split(" (")[0]
            places.setdefault((cat(t) or "분류 밖", name), []).append(f"{g.replace('Grade ', 'G')} {MONTHS[j][:3]}")
for g, j, t in WAITLIST:
    places.setdefault((cat(t) or "분류 밖", t[2:].split(" (")[0]), []).append(f"(후보) {g.replace('Grade ', 'G')} {MONTHS[j][:3]}")
order = CAT_NAMES + ["분류 밖"]
r = 2
for (cname, name), pl in sorted(places.items(), key=lambda x: (order.index(x[0][0]), x[0][1])):
    k.cell(r, 1, cname); k.cell(r, 2, name); k.cell(r, 3, ", ".join(pl)); r += 1
k.column_dimensions["A"].width = 22; k.column_dimensions["B"].width = 60; k.column_dimensions["C"].width = 40
k.freeze_panes = "A2"

w = wb.create_sheet("대기 후보")
for i, h in enumerate(["원래 학년", "원래 월", "분류", "주제 (실적)"], 1):
    c = w.cell(1, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = fill
w["A1"].comment = Comment("2026-10-19: 월 상한(그 달 수요일 수)을 넘어 앞·뒤 달로도 못 옮긴 주제. 캘린더 주제를 바꿀 때 교체 후보로 사용.", "Claude", width=320, height=80)
for r, (g, j, t) in enumerate(sorted(WAITLIST, key=lambda x: (x[1], GRADES.index(x[0]))), 2):
    for c, val in enumerate([g, MONTHS[j], cat(t) or "분류 밖", t], 1): w.cell(r, c, val)
w.column_dimensions["A"].width = 12; w.column_dimensions["C"].width = 22; w.column_dimensions["D"].width = 90
w.freeze_panes = "A2"

# ---------------------------------------------------------------
# 2026-10-16 사용자 요청: 원본 Var 탭에 붙여넣을 수 있게, 같은 레이아웃(M:AC, 같은 행 순서)으로
# 웨비나 행의 SF NLP1s(X)·#Deals(AB)·Revenue(AC)를 Events_OPS 값으로 바꾼 사본 탭.
# 바뀐 칸은 노란색, Var에 없던 Events_OPS 웨비나는 맨 아래 초록색 행으로 추가.
var_src = openpyxl.load_workbook(src_path)["Var"]
v = wb.create_sheet("Var (Events_OPS 반영)")
yellow = PatternFill("solid", fgColor="FFF2CC"); green = PatternFill("solid", fgColor="D9EAD3")
norm = lambda x: re.sub(r"\s+", " ", str(x or "")).strip().lower()
ops_by = {}
for o in kr: ops_by.setdefault(norm(o["name"]), o)  # 같은 이름 중복 시 첫 행(시트 위쪽)
last = 1
for row in var_src.iter_rows(min_row=1, max_row=var_src.max_row, max_col=29):
    for c in row:
        if c.value is not None:
            v.cell(c.row, c.column, c.value).number_format = c.number_format
            last = max(last, c.row)
used, changed = set(), 0
for r in range(2, last + 1):
    if v.cell(r, 14).value != "Webinar": continue
    o = ops_by.get(norm(v.cell(r, 19).value))
    if not o: continue
    used.add(norm(o["name"]))
    for col, val in ((24, o["nlp1"]), (28, o["deals"]), (29, round(o["rev"], 2))):
        if v.cell(r, col).value != val:
            v.cell(r, col, val).fill = yellow; changed += 1
added = 0
for o in kr:
    key = norm(o["name"])
    if key in used: continue
    used.add(key); last += 1; added += 1
    for col, val in ((14, "Webinar"), (19, o["name"]), (24, o["nlp1"]), (28, o["deals"]), (29, round(o["rev"], 2))):
        v.cell(last, col, val)
    for col in range(13, 30): v.cell(last, col).fill = green
for rr in range(2, last + 1): v.cell(rr, 29).number_format = '"$"#,##0'
v["M1"].comment = Comment(f"원본 Var 탭 사본. 웨비나 행의 SF NLP1s·#Deals·Revenue를 lead-tracker Events_OPS 값(Deal Tracker 기준, 2026-10-16 16:27 KST 덤프)으로 교체 — 노란색 = 바뀐 칸({changed}칸), 초록색 = Var에 없던 Events_OPS 웨비나({added}행). 해외 공동(SG/VN/HK 등)·세미나 행은 원본 그대로. M1부터 원본 Var 탭 M1에 그대로 붙여넣으면 됨.", "Claude", width=340, height=160)
v.freeze_panes = "M2"
print(f"VAR: changed cells {changed}, appended rows {added}, last row {last}")
wb.save(out_path)
print("rows", len(rows))
for g, cells in G.items():
    print(g, sum(len(x) for x in cells), "topics")
