import sys

new_mobile_code = """/* ============================================================
   MOBILE GATEWAY (new, additive — auto-shown on narrow viewports)
   Desktop app above this is untouched.
   ============================================================ */

function MobileRoleChoice({ onBack, onChoose }) {
  return (
    <div style={{ padding: "8px 18px 90px" }}>
      <ScreenHeader title="Sign in" onBack={onBack} />
      <div style={{ padding: "0 0 6px", fontSize: 12.5, color: COLOR.textSecondary, marginBottom: 16 }}>Are you signing in as a farmer, or as an authority-side user?</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <BigButton icon="🌾" title="Farmer login" subtitle="Report a problem, track your cases" onClick={() => onChoose("farmer")} />
        <BigButton icon="💻" title="Authority login" subtitle="Call console, authority, expert, surveillance or admin" variant="secondary" onClick={() => onChoose("authority")} />
      </div>
    </div>
  );
}

function MobileCredentialsForm({ role, onBack, onSignIn, showToast }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phase, setPhase] = useState("idle");

  const submit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;
    setPhase("hashing");
    await hashPassword(password);
    setPhase("signing");
    setTimeout(() => onSignIn(), 500);
  };

  return (
    <div style={{ padding: "8px 18px 90px" }}>
      <ScreenHeader title={`Sign in as ${role.label}`} onBack={onBack} />
      <form onSubmit={submit} style={{ marginTop: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
          <span style={{ fontSize: 26 }}>{role.icon}</span>
          <div style={{ fontSize: 12.5, color: COLOR.textSecondary }}>{role.sub}</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 10 }}>
          <div>
            <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginBottom: 5 }}>Email</div>
            <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder={`${role.id}@Krishi Seva.gov.in`} style={{ width: "100%", boxSizing: "border-box", padding: "12px 14px", borderRadius: 10, border: `1px solid ${COLOR.border}`, fontSize: 14 }} />
          </div>
          <div>
            <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginBottom: 5 }}>Password</div>
            <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" style={{ width: "100%", boxSizing: "border-box", padding: "12px 14px", borderRadius: 10, border: `1px solid ${COLOR.border}`, fontSize: 14 }} />
          </div>
        </div>
        <div style={{ fontSize: 10.5, color: COLOR.textMuted, marginBottom: 18 }}>🛡️ Password is hashed (SHA-256) in your browser before it's used.</div>
        <PrimaryBtn disabled={phase !== "idle"}>{phase === "hashing" ? "Encrypting…" : phase === "signing" ? "Signing in…" : "Sign in"}</PrimaryBtn>
        <div style={{ textAlign: "center", marginTop: 14 }}>
          <button type="button" onClick={() => showToast("OTP would be sent to the registered number")} style={{ background: "none", border: "none", color: COLOR.forest, fontSize: 12.5, fontWeight: 600, cursor: "pointer" }}>Login with OTP</button>
        </div>
      </form>
    </div>
  );
}

function MobileAuthorityBlock({ onBack, onForceDesktop }) {
  return (
    <div style={{ padding: "8px 18px 90px", textAlign: "center" }}>
      <ScreenHeader title="Authority Access" onBack={onBack} />
      <div style={{ marginTop: 40, marginBottom: 24, fontSize: 40 }}>💻</div>
      <h2 style={{ fontSize: 20, marginBottom: 12 }}>Desktop Required</h2>
      <p style={{ fontSize: 14, color: COLOR.textSecondary, marginBottom: 30, lineHeight: 1.5 }}>
        Sorry, you need a laptop or PC for authority access to view the complex maps, metrics, and tools.<br/><br/>
        Alternatively, you can force the application into desktop mode on your current device.
      </p>
      <PrimaryBtn onClick={onForceDesktop}>Start desktop mode</PrimaryBtn>
    </div>
  );
}

function MobileApp({ cases, addCase, updateCase, alerts, updateAlert, advisories, setAdvisories, a11y, setA11y, darkMode, setDarkMode, showToast, onViewDesktop, onBack }) {
  // view: roleChoice | farmerLogin | authorityBlock | farmerApp
  const [view, setView] = useState("roleChoice");
  const signOut = () => { setView("roleChoice"); };

  return (
    <div style={{ minHeight: "100dvh", background: COLOR.bg, fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', Arial, sans-serif" }}>
      {view === "farmerApp" ? (
        <FarmerRole cases={cases} addCase={addCase} updateCase={updateCase} advisories={advisories} embedded onSignOut={signOut} />
      ) : (
        <>
          {view === "roleChoice" && <MobileRoleChoice onBack={onBack} onChoose={(choice) => setView(choice === "farmer" ? "farmerLogin" : "authorityBlock")} />}
          {view === "farmerLogin" && <MobileCredentialsForm role={{ id: "farmer", label: "Farmer", sub: "Report a problem, track cases", icon: "🌾" }} onBack={() => setView("roleChoice")} onSignIn={() => setView("farmerApp")} showToast={showToast} />}
          {view === "authorityBlock" && <MobileAuthorityBlock onBack={() => setView("roleChoice")} onForceDesktop={onViewDesktop} />}
        </>
      )}
    </div>
  );
}
"""

new_app_code = """export default function App() {
  const isMobileDevice = useIsMobile();
  const [authed, setAuthed] = useState(false);
  const [publicMode, setPublicMode] = useState(isMobileDevice);
  const [activeRole, setActiveRole] = useState("authority");
  const [toast, setToast] = useState("");
  const [a11y, setA11y] = useState({ textLarge: false, highContrast: false, reducedMotion: false });
  const [darkMode, setDarkMode] = useState(false);
  const [forceDesktop, setForceDesktop] = useState(false);
  const [showMobileLogin, setShowMobileLogin] = useState(false);

  const [cases, setCases] = useState(INITIAL_CASES);
  const [alerts, setAlerts] = useState(INITIAL_ALERTS);
  const [advisories, setAdvisories] = useState(ADVISORIES_INIT);

  const showToast = (m) => { setToast(m); setTimeout(() => setToast(""), 2200); };
  const addCase = (c) => setCases((prev) => [c, ...prev]);
  const updateCase = (id, patch) => setCases((prev) => prev.map((c) => (c.id === id ? { ...c, ...patch } : c)));
  const updateAlert = (id, patch) => setAlerts((prev) => prev.map((a) => (a.id === id ? { ...a, ...patch } : a)));

  const signIn = (role) => { setAuthed(true); setPublicMode(false); setActiveRole(role); setShowMobileLogin(false); };
  const signOut = () => { setAuthed(false); setActiveRole("authority"); };

  const wrapperStyle = {
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', Arial, sans-serif",
    background: COLOR.bg, minHeight: "100vh", color: a11y.highContrast ? "#0A0C09" : COLOR.text,
    fontSize: a11y.textLarge ? "15px" : "13px",
    filter: themeFilter(darkMode, a11y.highContrast),
  };

  if (isMobileDevice && !forceDesktop && showMobileLogin) {
    return (
      <div style={wrapperStyle}>
        <GlobalStyles />
        <MobileApp
          cases={cases} addCase={addCase} updateCase={updateCase} alerts={alerts} updateAlert={updateAlert}
          advisories={advisories} setAdvisories={setAdvisories} a11y={a11y} setA11y={setA11y}
          darkMode={darkMode} setDarkMode={setDarkMode} showToast={showToast}
          onViewDesktop={() => { setShowMobileLogin(false); setForceDesktop(true); setPublicMode(false); }}
          onBack={() => setShowMobileLogin(false)}
        />
        <GlobalToast msg={toast} />
      </div>
    );
  }

  if (!authed && publicMode) {
    return (
      <div style={wrapperStyle}>
        <GlobalStyles />
        <PublicHeader onSignInClick={() => {
          if (isMobileDevice && !forceDesktop) setShowMobileLogin(true);
          else setPublicMode(false);
        }} darkMode={darkMode} setDarkMode={setDarkMode} />
        <PublicRole cases={cases} alerts={alerts} advisories={advisories} />
        <GlobalToast msg={toast} />
      </div>
    );
  }

  if (!authed) return <LoginScreen onSignIn={signIn} onViewPublic={() => setPublicMode(true)} showToast={showToast} darkMode={darkMode} setDarkMode={setDarkMode} />;

  return (
    <div style={wrapperStyle}>
      <GlobalStyles />
      <RoleSwitcherBar activeRole={activeRole} setActiveRole={setActiveRole} onSignOut={signOut} darkMode={darkMode} setDarkMode={setDarkMode} />

      {activeRole === "public" && <PublicRole cases={cases} alerts={alerts} advisories={advisories} />}
      {activeRole === "farmer" && <FarmerRole cases={cases} addCase={addCase} updateCase={updateCase} advisories={advisories} />}
      {activeRole === "call" && <CallConsoleRole cases={cases} updateCase={updateCase} showToast={showToast} />}
      {activeRole === "authority" && <AuthorityRole cases={cases} alerts={alerts} updateAlert={updateAlert} advisories={advisories} showToast={showToast} />}
      {activeRole === "expert" && <ExpertRole cases={cases} updateCase={updateCase} advisories={advisories} setAdvisories={setAdvisories} showToast={showToast} />}
      {activeRole === "surveillance" && <SurveillanceRole alerts={alerts} updateAlert={updateAlert} advisories={advisories} setAdvisories={setAdvisories} showToast={showToast} />}
      {activeRole === "admin" && <AdminRole a11y={a11y} setA11y={setA11y} showToast={showToast} />}

      <GlobalToast msg={toast} />
    </div>
  );
}
"""

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

start_token = '/* ============================================================'
idx = text.find('MOBILE GATEWAY (new, additive — auto-shown on narrow viewports)')
start_idx = text.rfind(start_token, 0, idx)

if start_idx != -1:
    new_text = text[:start_idx] + new_mobile_code + '\\n' + new_app_code
    with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Successfully updated the file!')
else:
    print('Could not find MOBILE GATEWAY block')
