import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace useIsMobile
old_use_is_mobile = """function useIsMobile() {
  const [isMobile, setIsMobile] = useState(() => typeof window !== "undefined" && window.innerWidth <= 768);
  useEffect(() => {
    const onResize = () => setIsMobile(window.innerWidth <= 768);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);
  return isMobile;
}"""

new_use_is_mobile = """function DesktopViewportForcer() {
  useEffect(() => {
    const meta = document.querySelector('meta[name="viewport"]');
    const originalContent = meta ? meta.getAttribute('content') : "width=device-width, initial-scale=1.0";
    if (meta) {
      meta.setAttribute('content', 'width=1024');
    }
    return () => {
      if (meta) {
        meta.setAttribute('content', originalContent);
      }
    };
  }, []);
  return null;
}

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const agent = typeof navigator !== "undefined" && /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    setIsMobile(agent);
  }, []);
  return isMobile;
}"""

if old_use_is_mobile not in text:
    print("Could not find old useIsMobile")
    sys.exit(1)

text = text.replace(old_use_is_mobile, new_use_is_mobile)

# 2. Add DesktopViewportForcer to the mobile gate default return
old_return = """    return (
      <div style={wrapperStyle}>
        <GlobalStyles />
        <PublicHeader onSignInClick={() => setMobileGate("choice")} darkMode={darkMode} setDarkMode={setDarkMode} />
        <PublicRole cases={cases} alerts={alerts} advisories={advisories} />
        <GlobalToast msg={toast} />
      </div>
    );
  }"""

new_return = """    return (
      <div style={wrapperStyle}>
        <DesktopViewportForcer />
        <GlobalStyles />
        <PublicHeader onSignInClick={() => setMobileGate("choice")} darkMode={darkMode} setDarkMode={setDarkMode} />
        <PublicRole cases={cases} alerts={alerts} advisories={advisories} />
        <GlobalToast msg={toast} />
      </div>
    );
  }"""

if old_return not in text:
    print("Could not find old return")
    sys.exit(1)

text = text.replace(old_return, new_return)

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated public dashboard viewport forcer")
