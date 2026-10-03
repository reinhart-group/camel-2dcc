import sys
from playwright.sync_api import sync_playwright
URL="http://giraffes-mac-mini.tail3a44c1.ts.net:8766/materials-science/student-demo.html"
def run(bt,tag,w,rule_idx,report,shots=True):
    b=bt.launch(); p=b.new_page(viewport={"width":w,"height":900}); errs=[]; n=[0]
    p.on("console", lambda m: errs.append(m.text) if m.type in("error","warning") else None); p.on("pageerror", lambda e: errs.append(str(e)))
    def shot(l):
        if shots: n[0]+=1; p.screenshot(path=f"l3-{tag}-{n[0]:02d}-{l}.png", full_page=True)
    p.goto(URL); p.wait_for_timeout(600); shot("prebrief")
    p.click("#skipIntro"); p.wait_for_timeout(500); shot("s1")
    # drag slider partway then show me
    p.locator("#cutoffRange").fill("0.6"); p.wait_for_timeout(300); shot("s1-drag")
    p.click("#checkCutoff"); p.wait_for_timeout(300); shot("s1-check-low"); print("  low:",p.inner_text("#foundNote")[:120])
    p.evaluate("(()=>{var r=document.getElementById('cutoffRange');r.value='0.93';r.dispatchEvent(new Event('input'))})()"); p.click("#checkCutoff"); p.wait_for_timeout(400); shot("s1-found"); print("  hit:",p.inner_text("#foundNote")[:160])
    p.click("#toLesson2"); p.wait_for_timeout(500); shot("s2")
    p.locator("#ruleChoices button, #ruleChoices label, #ruleChoices [role=radio]").nth(rule_idx).click(); p.wait_for_timeout(300)
    p.click("#revealRule"); p.wait_for_timeout(1200); shot("s2-reveal")
    p.click("#toLesson3"); p.wait_for_timeout(700)
    p.locator("input[name=shape][value=tail]").check(); p.locator("input[name=summary][value=resistant]").check(); p.wait_for_timeout(300); shot("s3")
    p.click("#toLesson4"); p.wait_for_timeout(500)
    p.locator(f"input[name=report][value={report}]").check(); p.fill("#reportNote","I trust Report B because it removed scans for how they were measured, not for their results."); p.wait_for_timeout(200); p.locator("input[name=flaw][value=cherry]").check(); p.wait_for_timeout(300); shot("s4")
    p.fill("#reportNote","I trust Report B because it removed scans for how they were measured, not for their results."); p.wait_for_timeout(200); p.click("#finishLesson"); p.wait_for_timeout(700); p.evaluate("document.getElementById('teacherDebrief').open=true"); shot("summary")
    print(tag,"| scrollW",p.evaluate("document.documentElement.scrollWidth"),"| errs",errs[:6])
    print("  ",p.inner_text("#studentSummary")[:400].replace("\n"," / ")); b.close()
with sync_playwright() as pw:
    run(pw.webkit,"wk",1280,1,"B")
    run(pw.webkit,"wkT",1280,2,"A",True)
    run(pw.chromium,"ph",390,0,"B")
