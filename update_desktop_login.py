import sys

new_login_screen = """function LoginScreen({ onSignIn, onViewPublic, showToast, darkMode, setDarkMode }) {
  // step: "groupChoice" | "authorityRoleChoice" | "credentials"
  const [step, setStep] = useState("groupChoice");
  const [role, setRole] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [phase, setPhase] = useState("idle");
  const [hashPreview, setHashPreview] = useState("");

  const chooseGroup = (group) => {
    if (group === "farmer") {
      const farmerRole = ROLES.find(r => r.id === "farmer");
      setRole(farmerRole);
      setStep("credentials");
    } else {
      setStep("authorityRoleChoice");
    }
  };

  const chooseRole = (r) => { setRole(r); setStep("credentials"); };

  const submit = async (e) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;
    setPhase("hashing");
    const hash = await hashPassword(password);
    setHashPreview(hash ? hash.slice(0, 16) + "…" : "");
    setPhase("signing");
    setTimeout(() => onSignIn(role.id), 500);
  };

  return (
    <div style={{ minHeight: "100vh", background: COLOR.bg, display: "flex", fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', Arial, sans-serif", position: "relative", filter: themeFilter(darkMode, false) }}>
      <GlobalStyles />
      <div style={{ position: "absolute", top: 16, right: 16, zIndex: 5 }}>
        <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} />
      </div>
      <div style={{ flex: 1, background: COLOR.forest, color: "#fff", padding: 48, display: "flex", flexDirection: "column", justifyContent: "center", minWidth: 320 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 30 }}>
          <div style={{ width: 34, height: 34, borderRadius: 8, background: "rgba(255,255,255,0.15)", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700 }}>K</div>
          <span style={{ fontSize: 17, fontWeight: 700 }}>Krishi Sevak</span>
        </div>
        <h1 style={{ fontSize: 30, fontWeight: 700, lineHeight: 1.25, margin: "0 0 14px", maxWidth: 380 }}>From farmer reports to early warning.</h1>
        <p style={{ fontSize: 14.5, color: "rgba(255,255,255,0.8)", maxWidth: 380, lineHeight: 1.6 }}>Helping veterinary teams respond faster to livestock health risks, while turning every report into useful public-health intelligence.</p>
        <div style={{ marginTop: 30 }}>
          <button onClick={onViewPublic} style={{ background: "rgba(255,255,255,0.12)", border: "1px solid rgba(255,255,255,0.25)", borderRadius: 8, padding: "10px 16px", color: "#fff", fontSize: 13, fontWeight: 600, cursor: "pointer" }}>
            🌐 View public dashboard, no login required
          </button>
        </div>
      </div>

      <div style={{ flex: 1.2, display: "flex", alignItems: "center", justifyContent: "center", padding: 32 }}>
        <div style={{ width: "100%", maxWidth: 420 }}>
          {step === "groupChoice" ? (
            <>
              <h2 style={{ fontSize: 19, fontWeight: 700, marginBottom: 6 }}>Sign in</h2>
              <div style={{ fontSize: 12.5, color: COLOR.textSecondary, marginBottom: 16 }}>Are you signing in as a farmer, or as an authority-side user?</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 18 }}>
                <BigButton icon="🌾" title="Farmer login" subtitle="Report a problem, track your cases" onClick={() => chooseGroup("farmer")} />
                <BigButton icon="🏛️" title="Authority login" subtitle="Call console, authority, expert, surveillance or admin" variant="secondary" onClick={() => chooseGroup("authority")} />
              </div>
              <div style={{ display: "inline-flex", alignItems: "center", gap: 6, fontSize: 10.5, fontWeight: 700, color: COLOR.clay, background: COLOR.clayTint, padding: "3px 9px", borderRadius: 16 }}>DEMO MODE</div>
            </>
          ) : step === "authorityRoleChoice" ? (
            <>
              <button type="button" onClick={() => setStep("groupChoice")} style={{ display: "flex", alignItems: "center", gap: 4, background: "none", border: "none", color: COLOR.forest, fontSize: 12.5, fontWeight: 600, cursor: "pointer", padding: 0, marginBottom: 14 }}>← Back</button>
              <h2 style={{ fontSize: 19, fontWeight: 700, marginBottom: 6 }}>Authority Access</h2>
              <div style={{ fontSize: 12.5, color: COLOR.textSecondary, marginBottom: 16 }}>Choose your specific authority role.</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 18 }}>
                {ROLES.filter(r => r.id !== "farmer").map((r) => {
                  const isAdmin = r.id === "admin";
                  return (
                    <button key={r.id} onClick={() => chooseRole(r)} style={{ display: "flex", alignItems: "center", gap: 8, padding: "12px", borderRadius: 10, border: isAdmin ? `2px solid ${COLOR.red}` : `1px solid ${COLOR.border}`, background: isAdmin ? COLOR.redTint : COLOR.surface, cursor: "pointer", textAlign: "left", position: "relative" }}>
                      <span style={{ fontSize: 18 }}>{r.icon}</span>
                      <span><div style={{ fontSize: 12.5, fontWeight: 700, color: isAdmin ? COLOR.red : COLOR.text }}>{r.label}</div><div style={{ fontSize: 10.5, color: COLOR.textMuted }}>{r.sub}</div></span>
                    </button>
                  );
                })}
              </div>
              <div style={{ display: "flex", gap: 12, alignItems: "flex-start", background: COLOR.surfaceSunken, padding: "12px 16px", borderRadius: 10, border: `1px solid ${COLOR.border}`, marginTop: 20 }}>
                <span style={{ fontSize: 20 }}>👉</span>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: COLOR.text }}>Login as Admin for full access (suggested for prototype version)</div>
                  <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginTop: 4 }}>This highlight and access will be removed when launched at full scale</div>
                </div>
              </div>
            </>
          ) : (
            <form onSubmit={submit}>
              <button type="button" onClick={() => { setStep(role.id === "farmer" ? "groupChoice" : "authorityRoleChoice"); setPhase("idle"); }} style={{ display: "flex", alignItems: "center", gap: 4, background: "none", border: "none", color: COLOR.forest, fontSize: 12.5, fontWeight: 600, cursor: "pointer", padding: 0, marginBottom: 14 }}>← Change role</button>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 18 }}>
                <span style={{ fontSize: 24 }}>{role.icon}</span>
                <div><div style={{ fontSize: 17, fontWeight: 700 }}>Sign in as {role.label}</div><div style={{ fontSize: 11.5, color: COLOR.textMuted }}>{role.sub}</div></div>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 8 }}>
                <div>
                  <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginBottom: 5 }}>Email</div>
                  <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder={`${role.id}@Krishi Sevak.gov.in`} style={{ width: "100%", boxSizing: "border-box", padding: "10px 12px", borderRadius: 8, border: `1px solid ${COLOR.border}`, fontSize: 13.5 }} />
                </div>
                <div>
                  <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginBottom: 5 }}>Password</div>
                  <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" style={{ width: "100%", boxSizing: "border-box", padding: "10px 12px", borderRadius: 8, border: `1px solid ${COLOR.border}`, fontSize: 13.5 }} />
                </div>
              </div>
              <div style={{ fontSize: 10.5, color: COLOR.textMuted, marginBottom: 16, display: "flex", alignItems: "center", gap: 5 }}>
                🛡️ Password is hashed (SHA-256) in your browser before it's used, a real deployment would also add HTTPS and server-side salted hashing.
              </div>
              <Button variant="primary" disabled={phase !== "idle"}>{phase === "hashing" ? "Encrypting…" : phase === "signing" ? "Signing in…" : "Sign in"}</Button>
              {hashPreview && phase === "signing" && <div style={{ fontSize: 10.5, color: COLOR.textMuted, marginTop: 8, fontFamily: "monospace" }}>hash: {hashPreview}</div>}
              <div style={{ textAlign: "center", margin: "12px 0 0" }}>
                <button type="button" onClick={() => showToast("OTP would be sent to the registered number")} style={{ background: "none", border: "none", color: COLOR.forest, fontSize: 12.5, fontWeight: 600, cursor: "pointer" }}>Login with OTP</button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}"""

new_role_switcher = """function RoleSwitcherBar({ activeRole, setActiveRole, onSignOut, darkMode, setDarkMode }) {
  if (activeRole !== "admin") {
    return (
      <div style={{ borderBottom: `1px solid ${COLOR.border}`, background: COLOR.surface, padding: "10px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 10 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 26, height: 26, borderRadius: 7, background: COLOR.forest, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 12 }}>K</div>
          <span style={{ fontSize: 13.5, fontWeight: 700 }}>Krishi Sevak</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} small />
          <button onClick={onSignOut} style={{ display: "flex", alignItems: "center", gap: 6, background: "none", border: `1px solid ${COLOR.border}`, borderRadius: 7, padding: "6px 11px", cursor: "pointer", fontSize: 12, color: COLOR.textSecondary }}><LogOut size={12} /> Sign out</button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ borderBottom: `1px solid ${COLOR.border}`, background: COLOR.surface, padding: "10px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 10 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <div style={{ width: 26, height: 26, borderRadius: 7, background: COLOR.forest, color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 700, fontSize: 12 }}>K</div>
        <span style={{ fontSize: 13.5, fontWeight: 700 }}>Krishi Sevak</span>
        <span style={{ display: "inline-flex", alignItems: "center", fontSize: 10, fontWeight: 700, color: COLOR.clay, background: COLOR.clayTint, padding: "2px 7px", borderRadius: 12, marginLeft: 4 }}>DEMO</span>
      </div>
      <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
        {ROLES.map((r) => (
          <button key={r.id} onClick={() => setActiveRole(r.id)} title={r.sub} className="ks-btn ks-tab-btn" style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 11px", borderRadius: 7, border: "none", cursor: "pointer", fontSize: 12.5, fontWeight: activeRole === r.id ? 700 : 500, background: activeRole === r.id ? COLOR.forestTint : "transparent", color: activeRole === r.id ? COLOR.forest : COLOR.textSecondary }}>
            <span>{r.icon}</span>{r.label}
          </button>
        ))}
        <button onClick={() => setActiveRole("public")} title="Public, read-only dashboard" className="ks-btn ks-tab-btn" style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 11px", borderRadius: 7, border: `1px dashed ${activeRole === "public" ? COLOR.forest : COLOR.border}`, cursor: "pointer", fontSize: 12.5, fontWeight: activeRole === "public" ? 700 : 500, background: activeRole === "public" ? COLOR.forestTint : "transparent", color: activeRole === "public" ? COLOR.forest : COLOR.textSecondary }}>
          <span>🌐</span>Public
        </button>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <DarkModeToggle darkMode={darkMode} setDarkMode={setDarkMode} small />
        <button onClick={onSignOut} style={{ display: "flex", alignItems: "center", gap: 6, background: "none", border: `1px solid ${COLOR.border}`, borderRadius: 7, padding: "6px 11px", cursor: "pointer", fontSize: 12, color: COLOR.textSecondary }}><LogOut size={12} /> Sign out</button>
      </div>
    </div>
  );
}"""

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find LoginScreen bounds
login_match = re.search(r'function LoginScreen\([^)]*\)\s*{', text)
if login_match:
    start_idx = login_match.start()
    count = 1
    end_idx = login_match.end()
    for i in range(end_idx, len(text)):
        if text[i] == '{': count += 1
        elif text[i] == '}': count -= 1
        if count == 0:
            login_end_idx = i + 1
            break
            
# Find RoleSwitcherBar bounds
role_match = re.search(r'function RoleSwitcherBar\([^)]*\)\s*{', text)
if role_match:
    r_start_idx = role_match.start()
    count = 1
    r_end_idx = role_match.end()
    for i in range(r_end_idx, len(text)):
        if text[i] == '{': count += 1
        elif text[i] == '}': count -= 1
        if count == 0:
            r_role_end_idx = i + 1
            break

# Replace both components
if login_match and role_match:
    # We must replace from bottom to top so indices don't change
    if r_start_idx > start_idx:
        text = text[:r_start_idx] + new_role_switcher + text[r_role_end_idx:]
        text = text[:start_idx] + new_login_screen + text[login_end_idx:]
    else:
        text = text[:start_idx] + new_login_screen + text[login_end_idx:]
        text = text[:r_start_idx] + new_role_switcher + text[r_role_end_idx:]

    with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully replaced components")
else:
    print("Could not find components")
