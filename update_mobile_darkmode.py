import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

start_sig = "  if (isMobileGateActive && !authed) {\n    if (mobileGate === \"choice\") {"
end_sig = "    return (\n      <div style={wrapperStyle}>\n        <GlobalStyles />\n        <PublicHeader"

start = text.find(start_sig)
if start == -1:
    print("Could not find mobile gate logic")
    sys.exit(1)

end = text.find(end_sig, start)
if end == -1:
    print("Could not find end of mobile gate logic")
    sys.exit(1)

new_comp = """  if (isMobileGateActive && !authed) {
    if (mobileGate === "choice") {
      return (
        <div style={wrapperStyle}>
          <GlobalStyles />
          <MobileRoleChoice onBack={() => setMobileGate(null)} darkMode={darkMode} setDarkMode={setDarkMode} onChoose={(choice) => setMobileGate(choice === "farmer" ? "farmerLogin" : "authorityBlocked")} />
        </div>
      );
    }
    if (mobileGate === "farmerLogin") {
      return (
        <div style={wrapperStyle}>
          <GlobalStyles />
          <MobileFarmerLogin onBack={() => setMobileGate("choice")} onSignIn={() => { setMobileGate(null); signIn("farmer"); }} showToast={showToast} darkMode={darkMode} setDarkMode={setDarkMode} />
          <GlobalToast msg={toast} />
        </div>
      );
    }
    if (mobileGate === "authorityBlocked") {
      return (
        <div style={wrapperStyle}>
          <GlobalStyles />
          <MobileAuthorityBlocked onBack={() => setMobileGate("choice")} darkMode={darkMode} setDarkMode={setDarkMode} />
        </div>
      );
    }
"""

text = text[:start] + new_comp + text[end:]

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated mobile gates with wrapperStyle")
