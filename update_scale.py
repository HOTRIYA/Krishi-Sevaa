import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Replace DesktopViewportForcer definition
old_def = """function DesktopViewportForcer() {
  useEffect(() => {
    const meta = document.querySelector('meta[name="viewport"]');
    const originalContent = meta ? meta.getAttribute('content') : "width=device-width, initial-scale=1.0";
    if (meta) {
      meta.setAttribute('content', 'width=1024, initial-scale=0.1, maximum-scale=10.0');
    }
    return () => {
      if (meta) {
        meta.setAttribute('content', originalContent);
      }
    };
  }, []);
  return null;
}"""

new_def = """function DesktopScaleWrapper({ children }) {
  const [scale, setScale] = useState(1);
  useEffect(() => {
    const onResize = () => {
      setScale(window.innerWidth < 1024 ? window.innerWidth / 1024 : 1);
    };
    onResize();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return (
    <div style={{ zoom: scale, minWidth: 1024, overflowX: "hidden", minHeight: "100vh" }}>
      {children}
    </div>
  );
}"""

if old_def in text:
    text = text.replace(old_def, new_def)
else:
    print("Could not find DesktopViewportForcer definition")
    sys.exit(1)


# 2. Replace the usage
old_usage = """    return (
      <div style={wrapperStyle}>
        <DesktopViewportForcer />
        <GlobalStyles />
        <PublicHeader onSignInClick={() => setMobileGate("choice")} darkMode={darkMode} setDarkMode={setDarkMode} />
        <PublicRole cases={cases} alerts={alerts} advisories={advisories} />
        <GlobalToast msg={toast} />
      </div>
    );"""

new_usage = """    return (
      <div style={wrapperStyle}>
        <DesktopScaleWrapper>
          <GlobalStyles />
          <PublicHeader onSignInClick={() => setMobileGate("choice")} darkMode={darkMode} setDarkMode={setDarkMode} />
          <PublicRole cases={cases} alerts={alerts} advisories={advisories} />
        </DesktopScaleWrapper>
        <GlobalToast msg={toast} />
      </div>
    );"""

if old_usage in text:
    text = text.replace(old_usage, new_usage)
else:
    print("Could not find DesktopViewportForcer usage")
    sys.exit(1)

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated to DesktopScaleWrapper")
