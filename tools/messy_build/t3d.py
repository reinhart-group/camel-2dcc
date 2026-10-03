from playwright.sync_api import sync_playwright
URL="http://giraffes-mac-mini.tail3a44c1.ts.net:8766/materials-science/student-demo.html"
with sync_playwright() as pw:
  for name,bt in [("webkit",pw.webkit),("chromium",pw.chromium)]:
    b=bt.launch(); p=b.new_page(viewport={"width":1280,"height":1000}); logs=[]
    p.on("console", lambda m: logs.append(m.type+": "+m.text)); p.on("pageerror", lambda e: logs.append("pageerror "+str(e)))
    p.goto(URL); p.wait_for_timeout(400); p.locator("#intro button:visible").last.click(); p.wait_for_timeout(6000)
    box=p.locator("#surf1 .plot3d").bounding_box()
    p.mouse.move(box["x"]+box["width"]/2,box["y"]+box["height"]/2); p.mouse.down(); p.mouse.move(box["x"]+box["width"]/2+120,box["y"]+box["height"]/2+20,steps=8); p.mouse.up(); p.wait_for_timeout(800)
    p.screenshot(path=f"live3d-{name}.png")
    print(name, p.inner_text("#surf0status"), "|", p.inner_text("#surf1status")); print("  ", [l for l in logs if "[3d]" in l or "error" in l.lower()][:8]); b.close()
