import sys
import re

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update LanguageTourBtn to LanguageTourWrapper
old_tour = """function LanguageTourBtn() {
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
      <style>{`
        @keyframes ksFloatTour {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-4px); }
        }
      `}</style>
      <button style={{ background: "rgba(255,255,255,0.15)", border: "none", color: "#fff", borderRadius: 8, padding: "5px 10px", fontSize: 13, fontWeight: 600, cursor: "pointer", display: "flex", alignItems: "center", gap: 4 }}>
        🌐 EN
      </button>
      {showTour && (
        <div style={{ 
          position: "absolute", top: "120%", right: 0, 
          background: COLOR.blue, color: "#fff", padding: "10px 14px", 
          borderRadius: 8, fontSize: 13, fontWeight: 600, width: 200, 
          boxShadow: "0 8px 24px rgba(0,0,0,0.2)", zIndex: 1000,
          animation: "ksFloatTour 2.5s infinite ease-in-out"
        }}>
          <div style={{ position: "absolute", top: -6, right: 15, width: 12, height: 12, background: COLOR.blue, transform: "rotate(45deg)" }}></div>
          Change language from here
        </div>
      )}
    </div>
  );
}"""

new_tour = """function LanguageTourWrapper({ children }) {
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
    <div style={{ position: "relative", display: "flex", alignItems: "center" }}>
      <style>{`
        @keyframes ksFloatTour {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-4px); }
        }
      `}</style>
      {children}
      {showTour && (
        <div style={{ 
          position: "absolute", top: "120%", right: 0, 
          background: COLOR.blue, color: "#fff", padding: "10px 14px", 
          borderRadius: 8, fontSize: 13, fontWeight: 600, width: 200, 
          boxShadow: "0 8px 24px rgba(0,0,0,0.2)", zIndex: 1000,
          animation: "ksFloatTour 2.5s infinite ease-in-out"
        }}>
          <div style={{ position: "absolute", top: -6, right: 15, width: 12, height: 12, background: COLOR.blue, transform: "rotate(45deg)" }}></div>
          Change language from here
        </div>
      )}
    </div>
  );
}"""

if old_tour in text:
    text = text.replace(old_tour, new_tour)
else:
    print("Could not find LanguageTourBtn")
    sys.exit(1)


# 2. Remove rightExtra from MobileFarmerLogin
old_farmer_header = """<MobileGateHeader title="Sign in as Farmer" onBack={onBack} darkMode={darkMode} setDarkMode={setDarkMode} rightExtra={<LanguageTourBtn />} />"""
new_farmer_header = """<MobileGateHeader title="Sign in as Farmer" onBack={onBack} darkMode={darkMode} setDarkMode={setDarkMode} />"""

if old_farmer_header in text:
    text = text.replace(old_farmer_header, new_farmer_header)
else:
    print("Could not find MobileFarmerLogin header")
    sys.exit(1)


# 3. Add LanguageTourWrapper to FarmerRole
old_farmer_lang_btn = """<button onClick={() => setLang((l) => (l === "en" ? "hi" : "en"))} style={{ background: "none", border: "none", fontSize: 11.5, fontWeight: 700, color: COLOR.forest, cursor: "pointer" }}>{lang === "en" ? "हिंदी" : "English"}</button>"""
new_farmer_lang_btn = """<LanguageTourWrapper>
              <button onClick={() => setLang((l) => (l === "en" ? "hi" : "en"))} style={{ background: "none", border: "none", fontSize: 11.5, fontWeight: 700, color: COLOR.forest, cursor: "pointer" }}>{lang === "en" ? "हिंदी" : "English"}</button>
            </LanguageTourWrapper>"""

if old_farmer_lang_btn in text:
    text = text.replace(old_farmer_lang_btn, new_farmer_lang_btn)
else:
    print("Could not find FarmerRole lang button")
    sys.exit(1)

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully moved language tour")
