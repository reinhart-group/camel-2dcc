from playwright.sync_api import sync_playwright
URL="http://giraffes-mac-mini.tail3a44c1.ts.net:8766/materials-science/investigation.html"
tabs=["warmup","notice","mess","model","dials","reflect"]
with sync_playwright() as pw:
  for w in (1280,390):
    b=pw.webkit.launch(); p=b.new_page(viewport={"width":w,"height":900}); errs=[]
    p.on("console", lambda m: errs.append(m.text) if m.type=="error" else None); p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(URL); p.wait_for_timeout(1500)
    for t in tabs:
      p.evaluate(f"switchTab('{t}')"); p.wait_for_timeout(700)
      p.screenshot(path=f"mz-{w}-{t}.png", full_page=True)
    print(w,"errs",errs[:5],"scrollW",p.evaluate("document.documentElement.scrollWidth")); b.close()
