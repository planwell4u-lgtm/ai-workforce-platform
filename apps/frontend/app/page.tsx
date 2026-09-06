/* eslint-disable @next/next/no-html-link-for-pages */

const spaces = [
  ["Support Assistant", "Answers approved support questions and offers a governed route when human support is available.", "Open Support", "/support", "Available"],
  ["Sales Assistant", "Provides approved sales information and carefully scoped sales conversations.", "Open Sales", "/sales", "Available"],
  ["Front Desk Routes", "Lets authorised administrators manage test-only web-chat routing destinations.", "Manage routes", "/front-desk-admin", "Admin"],
  ["Access Management", "Lets the owner grant Support and Front Desk access to existing users.", "Manage access", "/access-management", "Owner"],
  ["Local Management", "Gives workspace owners a read-only view of the cloud pilot, access controls, and operational checks.", "Open management", "/local-management", "Owner"],
];

export default function Home() {
  return <main className="landing-page">
    <header className="landing-nav"><a href="/" className="landing-brand">PLANWELL</a><nav aria-label="Primary navigation"><a href="/support">Support</a><a href="/sales">Sales</a><a href="/front-desk-admin">Front Desk</a><a href="/access-management">Access</a><a href="/local-management">Management</a></nav><a href="/support" className="landing-button landing-button-small">Open workspace</a></header>
    <section className="landing-hero"><p className="landing-eyebrow">GOVERNED AI WORKSPACE</p><h1>Helpful conversations.<br/><span>Clear operational boundaries.</span></h1><p className="landing-intro">Planwell brings approved support knowledge, sales assistance, and controlled routing into one practical workspace.</p><div className="landing-actions"><a href="/support" className="landing-button">Try Support →</a><a href="/front-desk-admin" className="landing-button landing-button-quiet">View Front Desk</a></div><p className="landing-note">Do not share passwords or payment details in chat.</p></section>
    <section className="landing-workspace" aria-labelledby="workspace-title"><div className="workspace-heading"><div><p className="landing-eyebrow">WORKSPACE OVERVIEW</p><h2 id="workspace-title">Choose the right controlled experience.</h2></div><span className="landing-status"><i/>Local workspace ready</span></div><div className="capability-grid">{spaces.map(([title,text,action,href,status]) => <article className="capability-card" key={title}><div className="capability-top"><span>WORKSPACE</span><b>{status}</b></div><h3>{title}</h3><p>{text}</p><div className="capability-boundary"><strong>Boundary:</strong> Access is limited to the approved role, knowledge, and route for this workspace.</div><a href={href} className="capability-link">{action} →</a></article>)}</div></section>
    <section className="landing-boundaries"><p className="landing-eyebrow">BUILT FOR CONTROL</p><h2>Useful when it is allowed. Clear when it is not.</h2><div><p><strong>Approved knowledge</strong><br/>Responses are based on the information available to the assigned workspace.</p><p><strong>Role-aware access</strong><br/>Support users and Front Desk administrators use their appropriate sign-in permissions.</p><p><strong>Test-focused routing</strong><br/>Front Desk routing remains within the configured test-only web-chat environment.</p></div></section>
    <footer className="landing-footer"><span>PLANWELL</span><span>Governed workspace • Local environment</span></footer>
  </main>;
}
