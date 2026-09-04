import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

start_sig = "function MobileAuthorityBlocked({ onBack, darkMode, setDarkMode }) {"
end_sig = "  );\n}\n"

start = text.find(start_sig)
if start == -1:
    print("Could not find MobileAuthorityBlocked")
    sys.exit(1)

end = text.find(end_sig, start)
if end == -1:
    print("Could not find end of MobileAuthorityBlocked")
    sys.exit(1)

new_comp = """function MobileAuthorityBlocked({ onBack, darkMode, setDarkMode }) {
  const [showDesktopAlert, setShowDesktopAlert] = useState(false);
  const [wobble, setWobble] = useState(false);
  const [localToast, setLocalToast] = useState("");

  const handleDoneIt = () => {
    setWobble(true);
    setLocalToast("Please change to desktop mode from your browser settings!");
    setTimeout(() => setWobble(false), 500);
    setTimeout(() => setLocalToast(""), 3000);
  };

  return (
    <div style={{ minHeight: "100dvh", background: COLOR.bg }}>
      <style>
        {`
          @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
            20%, 40%, 60%, 80% { transform: translateX(4px); }
          }
          @keyframes slideUp {
            from { opacity: 0; transform: translate(-50%, 20px); }
            to { opacity: 1; transform: translate(-50%, 0); }
          }
        `}
      </style>
      <MobileGateHeader title="Authority login" onBack={onBack} darkMode={darkMode} setDarkMode={setDarkMode} />
      <div style={{ padding: "24px 18px 90px" }}>
        <div style={{ background: COLOR.amberTint, border: `1px solid ${COLOR.amber}33`, borderRadius: 14, padding: 20, marginBottom: 20 }}>
          <div style={{ fontSize: 30, marginBottom: 10 }}>💻</div>
          <div style={{ fontSize: 15, fontWeight: 700, color: COLOR.text, marginBottom: 6 }}>Sorry, you need a laptop or PC for authority access</div>
          <div style={{ fontSize: 13, color: COLOR.textSecondary, lineHeight: 1.6 }}>The Call Console, Authority, Expert, Surveillance and Admin workspaces are built for larger screens. You can still use them from this phone by switching to desktop mode below.</div>
        </div>
        <PrimaryBtn onClick={() => setShowDesktopAlert(true)}><span style={{ display: "inline-flex", alignItems: "center", gap: 8 }}><Monitor size={16} /> Start desktop mode</span></PrimaryBtn>
        <div style={{ textAlign: "center", marginTop: 14 }}>
          <button type="button" onClick={onBack} style={{ background: "none", border: "none", color: COLOR.textSecondary, fontSize: 12.5, fontWeight: 600, cursor: "pointer" }}>← Go back</button>
        </div>
      </div>
      {showDesktopAlert && (
        <Modal title="Switch to Desktop Mode" onClose={() => setShowDesktopAlert(false)}>
          <div style={{ fontSize: 13, color: COLOR.text, lineHeight: 1.6, animation: wobble ? "shake 0.5s ease-in-out" : "none" }}>
            <div style={{ marginBottom: 12 }}>To view the authority dashboards on your phone, you must manually enable "Desktop site" in your mobile browser.</div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>For Chrome / Android:</div>
            <div style={{ marginBottom: 12, color: COLOR.textSecondary }}>Tap the three dots (<span style={{ fontWeight: 700 }}>⋮</span>) in the top right corner and check the box for <span style={{ fontWeight: 700 }}>"Desktop site"</span>.</div>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>For Safari / iOS:</div>
            <div style={{ marginBottom: 16, color: COLOR.textSecondary }}>Tap the <span style={{ fontWeight: 700 }}>"aA"</span> icon in the address bar and select <span style={{ fontWeight: 700 }}>"Request Desktop Website"</span>.</div>
            <PrimaryBtn onClick={handleDoneIt}>I've done it, continue</PrimaryBtn>
          </div>
        </Modal>
      )}
      {localToast && (
        <div style={{ position: "fixed", bottom: 40, left: "50%", transform: "translateX(-50%)", background: COLOR.forest, color: "#fff", padding: "10px 14px", borderRadius: 8, fontSize: 12, fontWeight: 600, zIndex: 100000, animation: "slideUp 0.3s ease-out", boxShadow: "0 4px 12px rgba(0,0,0,0.15)", whiteSpace: "normal", textAlign: "center", width: "max-content", maxWidth: "90%", pointerEvents: "none" }}>
          {localToast}
        </div>
      )}
    </div>
  );
}
"""

text = text[:start] + new_comp + text[end+len(end_sig):]

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated MobileAuthorityBlocked with modal shaking and fixed toast")
