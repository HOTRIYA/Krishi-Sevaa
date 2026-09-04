import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# We need to change the 'authorityRoleChoice' step in LoginScreen
# First, let's find that block.
# Currently it looks like:
#           ) : step === "authorityRoleChoice" ? (
#             <>
#               <button type="button" onClick={() => setStep("groupChoice")} ... >← Back</button>
#               <h2 style={{ fontSize: 19, fontWeight: 700, marginBottom: 6 }}>Authority Access</h2>
#               <div style={{ fontSize: 12.5, color: COLOR.textSecondary, marginBottom: 16 }}>Choose your specific authority role.</div>
#               <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 18 }}>
#                 {ROLES.filter(r => r.id !== "farmer").map((r) => { ... })}
#               </div>
#               <div style={{ display: "flex", gap: 12, alignItems: "flex-start", background: COLOR.surfaceSunken, padding: "12px 16px", borderRadius: 10, border: `1px solid ${COLOR.border}`, marginTop: 20 }}>
#                 ...
#               </div>
#             </>
#           ) : (

new_authority_block = """          ) : step === "authorityRoleChoice" ? (
            <>
              <button type="button" onClick={() => setStep("groupChoice")} style={{ display: "flex", alignItems: "center", gap: 4, background: "none", border: "none", color: COLOR.forest, fontSize: 12.5, fontWeight: 600, cursor: "pointer", padding: 0, marginBottom: 14 }}>← Back</button>
              <h2 style={{ fontSize: 19, fontWeight: 700, marginBottom: 6 }}>Authority Access</h2>
              <div style={{ fontSize: 12.5, color: COLOR.textSecondary, marginBottom: 16 }}>Choose your specific authority role.</div>
              
              <div style={{ display: "flex", gap: 12, alignItems: "flex-start", background: COLOR.surfaceSunken, padding: "12px 16px", borderRadius: 10, border: `1px solid ${COLOR.border}`, marginBottom: 12 }}>
                <span style={{ fontSize: 20 }}>👉</span>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: COLOR.text }}>Login as Admin for full access (suggested for prototype version)</div>
                  <div style={{ fontSize: 11.5, color: COLOR.textMuted, marginTop: 4 }}>This highlight and access will be removed when launched at full scale</div>
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 18 }}>
                {ROLES.filter(r => r.id !== "farmer").sort((a, b) => a.id === "admin" ? -1 : b.id === "admin" ? 1 : 0).map((r) => {
                  const isAdmin = r.id === "admin";
                  return (
                    <button key={r.id} onClick={() => chooseRole(r)} style={{ display: "flex", alignItems: "center", gap: 8, padding: "12px", borderRadius: 10, border: isAdmin ? `2px solid ${COLOR.red}` : `1px solid ${COLOR.border}`, background: isAdmin ? COLOR.redTint : COLOR.surface, cursor: "pointer", textAlign: "left", position: "relative", gridColumn: isAdmin ? "1 / -1" : "auto" }}>
                      <span style={{ fontSize: 18 }}>{r.icon}</span>
                      <span><div style={{ fontSize: 12.5, fontWeight: 700, color: isAdmin ? COLOR.red : COLOR.text }}>{r.label}</div><div style={{ fontSize: 10.5, color: COLOR.textMuted }}>{r.sub}</div></span>
                    </button>
                  );
                })}
              </div>
            </>
          ) : ("""

import re

# Match the old authority choice block
start_str = ') : step === "authorityRoleChoice" ? ('
end_str = ') : ('

start_idx = text.find(start_str)
if start_idx != -1:
    end_idx = text.find(end_str, start_idx + len(start_str))
    if end_idx != -1:
        text = text[:start_idx] + new_authority_block + text[end_idx + len(end_str):]
        with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Updated authorityRoleChoice layout successfully.")
    else:
        print("Could not find end of block.")
else:
    print("Could not find start of block.")
