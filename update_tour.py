import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Inject the LanguageTourBtn component right before MobileGateHeader
lang_btn = """function LanguageTourBtn() {
  const [showTour, setShowTour] = useState(true);

  useEffect(() => {
    if (!showTour) return;
    const hide = () => setShowTour(false);
    window.addEventListener("touchstart", hide, { capture: true, once: true });
    window.addEventListener("mousedown", hide, { capture: true, once: true });
    window.addEventListener("scroll", hide, { capture: true, once: true });
    return () => {
      window.removeEventListener("touchstart", hide, { capture: true });
      window.removeEventListener("mousedown", hide, { capture: true });
      window.removeEventListener("scroll", hide, { capture: true });
    };
  }, [showTour]);

  return (
    <div style={{ position: "relative" }}>
      <button style={{ background: "rgba(255,255,255,0.15)", border: "none", color: "#fff", borderRadius: 8, padding: "5px 10px", fontSize: 13, fontWeight: 600, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
        🌐 EN
      </button>
      {showTour && (
        <div style={{ 
          position: "absolute", top: "120%", right: 0, 
          background: COLOR.blue, color: "#fff", padding: "10px 14px", 
          borderRadius: 8, fontSize: 13, fontWeight: 600, width: 200, 
          boxShadow: "0 8px 24px rgba(0,0,0,0.2)", zIndex: 1000,
          animation: "float 2s infinite ease-in-out"
        }}>
          <div style={{ position: "absolute", top: -6, right: 15, width: 12, height: 12, background: COLOR.blue, transform: "rotate(45deg)" }}></div>
          Change language from here
        </div>
      )}
    </div>
  );
}

function MobileGateHeader({ title, onBack, darkMode, setDarkMode, rightExtra }) {"""

old_header_def = "function MobileGateHeader({ title, onBack, darkMode, setDarkMode }) {"
if old_header_def in text:
    text = text.replace(old_header_def, lang_btn)
else:
    print("Could not find old_header_def")
    sys.exit(1)

old_header_body = """    <div style={{ background: COLOR.forest, color: "#fff", padding: "14px 16px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, minWidth: 0 }}>
        <button onClick={onBack} style={{ background: "none", border: "none", color: "#fff", fontSize: 20, cursor: "pointer", padding: 0, width: 24 }}> </button>
        <span style={{ fontSize: 15.5, fontWeight: 700 }}>{title}</span>
      </div>
      <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} small />
    </div>"""

new_header_body = """    <div style={{ background: COLOR.forest, color: "#fff", padding: "14px 16px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, minWidth: 0 }}>
        <button onClick={onBack} style={{ background: "none", border: "none", color: "#fff", fontSize: 20, cursor: "pointer", padding: 0, width: 24 }}>←</button>
        <span style={{ fontSize: 15.5, fontWeight: 700 }}>{title}</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        {rightExtra}
        <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} small />
      </div>
    </div>"""

# Sometimes the back button has a different character, let's just use string slicing or regex.
import re
text = re.sub(r'<div style=\{\{ background: COLOR\.forest, color: "#fff", padding: "14px 16px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 \}\}>.*?<DarkModeToggle darkMode=\{darkMode\} setDarkMode=\{setDarkMode\} small />\s*</div>', new_header_body, text, flags=re.DOTALL)

# 3. Add rightExtra={<LanguageTourBtn />} to MobileFarmerLogin
old_farmer_header = """<MobileGateHeader title="Sign in as Farmer" onBack={onBack} darkMode={darkMode} setDarkMode={setDarkMode} />"""
new_farmer_header = """<MobileGateHeader title="Sign in as Farmer" onBack={onBack} darkMode={darkMode} setDarkMode={setDarkMode} rightExtra={<LanguageTourBtn />} />"""

if old_farmer_header in text:
    text = text.replace(old_farmer_header, new_farmer_header)
else:
    print("Could not find MobileFarmerLogin header")
    sys.exit(1)

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added LanguageTourBtn")
