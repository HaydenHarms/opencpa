import { Link } from 'react-router-dom';

const UPDATED = 'October 2, 2026';
const ISSUES = 'https://github.com/HaydenHarms/opencpa/issues';
const REPO = 'https://github.com/HaydenHarms/opencpa';

/** /privacy */
export function Privacy() {
  return (
    <section className="prose legal">
      <h1>Privacy Policy</h1>
      <p className="muted">Last updated {UPDATED}</p>
      <p>
        OpenCPA is a free, open-source CPA exam study site run by Hayden Harms. This page explains
        what the site stores about you, why, and how to delete it. The short version: we keep only
        what the study features need, we don’t show ads, we don’t sell or share your data for
        marketing, and the site has no analytics or tracking scripts.
      </p>

      <h2>What we store</h2>
      <ul>
        <li>
          <b>Your study activity:</b> the questions and simulations you answer, what you answered,
          your score, how long you took, your practice sessions and your review schedule.
        </li>
        <li>
          <b>A random device ID</b> kept in your browser, which links that activity to you while
          you’re not signed in. It contains nothing about who you are.
        </li>
        <li>
          <b>If you sign in with GitHub:</b> your GitHub user ID, username, display name and primary
          verified email address. We never see your GitHub password and we don’t keep GitHub’s
          access token after sign-in.
        </li>
        <li>
          <b>If you sign in by email:</b> your email address. To limit abuse, we briefly keep a
          record of each sign-in link sent (a hash, not the link itself); these are cleared out
          after about a day.
        </li>
        <li>
          <b>Sign-in sessions:</b> a random token kept in your browser so you stay signed in. We
          store only a one-way hash of it.
        </li>
        <li>
          <b>Claude connector link</b>, if you make one: stored only as a one-way hash, with when it
          was made and last used.
        </li>
      </ul>
      <p>
        The site uses your browser’s local storage for the device ID, the sign-in token and small
        preferences such as your last-chosen exam section. It doesn’t use cookies.
      </p>

      <h2>How we use it</h2>
      <p>
        Only to run the site: grading, choosing the next questions, scheduling reviews, showing your
        progress, keeping you signed in, and answering lookups from your Claude connector. We don’t
        use it for advertising, and we don’t sell it or share it with anyone for marketing.
      </p>

      <h2>Services that handle it</h2>
      <ul>
        <li>
          <b>Cloudflare</b> hosts the site, the API and the database. Like any web host, it handles
          your IP address and request details to deliver the site and protect it from abuse.
        </li>
        <li>
          <b>GitHub</b>, if you sign in with it, under GitHub’s own privacy statement.
        </li>
        <li>
          <b>Resend</b> sends sign-in emails, if you sign in by email. It receives your email
          address and the message.
        </li>
        <li>
          <b>Claude (Anthropic)</b>, only if you connect it from the{' '}
          <Link to="/claude">Claude page</Link>. Claude then reads your OpenCPA questions, answers
          and progress through your own Claude account, under Anthropic’s terms and privacy policy.
          You can disconnect it at any time.
        </li>
      </ul>
      <p>
        We may disclose information if the law requires it. If OpenCPA ever changes hands, this
        policy would continue to apply to the data collected under it.
      </p>

      <h2>How long we keep it, and deleting it</h2>
      <p>
        We keep your data until you delete it. On the <Link to="/account">Account page</Link> you
        can delete your account, or, if you’re not signed in, this device’s data. Deleting removes
        your answers, review schedule, sessions, Claude connector link and sign-ins right away, and
        it can’t be undone. You can also ask us to delete or export your data through the contact
        below.
      </p>

      <h2>Security</h2>
      <p>
        Data is sent over HTTPS, and sign-in tokens and connector links are stored only as hashes.
        No system is perfectly secure; if we learn of a breach affecting your data, we’ll say so on
        the site.
      </p>

      <h2>Children</h2>
      <p>
        OpenCPA is meant for people preparing for the CPA exam and isn’t directed at children under
        13. We don’t knowingly collect their information; if you believe a child has signed up,
        contact us and we’ll delete it.
      </p>

      <h2>Your rights</h2>
      <p>
        Depending on where you live, you may have the right to see, correct, export or delete your
        data. Use the Account page or contact us, and we’ll help.
      </p>

      <h2>Changes</h2>
      <p>
        If this policy changes, we’ll update the date at the top. The full history is public in the
        site’s <a href={REPO}>source code repository</a>.
      </p>

      <h2>Contact</h2>
      <p>
        Open an issue at <a href={ISSUES}>github.com/HaydenHarms/opencpa/issues</a>. For anything
        private, say so in the issue without the details, and we’ll reply with a private way to
        reach us.
      </p>
    </section>
  );
}

/** /terms */
export function Terms() {
  return (
    <section className="prose legal">
      <h1>Terms of Use</h1>
      <p className="muted">Last updated {UPDATED}</p>
      <p>
        These terms cover your use of OpenCPA (opencpa.pages.dev), a free, open-source CPA exam
        study site run by Hayden Harms. By using the site you agree to them. If you don’t agree,
        please don’t use it.
      </p>

      <h2>Not an official exam resource</h2>
      <p>
        OpenCPA is an independent project. It isn’t affiliated with, endorsed by or sponsored by the
        American Institute of Certified Public Accountants (AICPA), the National Association of
        State Boards of Accountancy (NASBA), any state board of accountancy, or any commercial
        review course. “Uniform CPA Examination” and related marks belong to their owners. The
        questions here are original practice material written for OpenCPA, not actual or released
        exam questions.
      </p>

      <h2>Study aid only</h2>
      <p>
        The questions, explanations, scores and progress estimates are for practice. They may
        contain mistakes or fall behind changes in accounting standards and the exam blueprint, and
        they don’t predict your exam result. Nothing on the site is professional accounting, tax,
        legal or financial advice. Check important points against the authoritative standards.
      </p>
      <p>
        If you think a question or answer is wrong, please{' '}
        <a href="https://github.com/HaydenHarms/opencpa/issues">report it</a>.
      </p>

      <h2>Your account</h2>
      <p>
        You can use OpenCPA without an account. If you sign in, keep your GitHub account or email
        secure, since anyone who controls it can sign in as you. Treat your Claude connector link
        like a password. You can delete your account at any time on the{' '}
        <Link to="/account">Account page</Link>.
      </p>

      <h2>Acceptable use</h2>
      <p>Please don’t:</p>
      <ul>
        <li>
          overload, attack or try to break into the site, or get around its limits (for example with
          automated mass requests or scraping);
        </li>
        <li>access other people’s data or accounts;</li>
        <li>use the site for anything unlawful.</li>
      </ul>
      <p>We may limit or close access for anyone who does.</p>

      <h2>Content and code licenses</h2>
      <p>
        OpenCPA’s questions and explanations are licensed under{' '}
        <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>, and its code
        under the MIT License. You may reuse them under those licenses, with attribution. The source
        is at <a href={REPO}>github.com/HaydenHarms/opencpa</a>.
      </p>

      <h2>Claude</h2>
      <p>
        The optional Claude connector lets Claude read your OpenCPA progress through your own Claude
        account. Your use of Claude is between you and Anthropic, under their terms. OpenCPA grades
        your answers; Claude’s explanations are its own, and it can be wrong.
      </p>

      <h2>No warranty</h2>
      <p>
        The site is provided free, “as is” and “as available”, without warranties of any kind,
        express or implied, including accuracy, fitness for a particular purpose and
        non-infringement. It may change, have downtime, or stop, and we don’t promise to keep your
        data forever.
      </p>

      <h2>Limitation of liability</h2>
      <p>
        To the fullest extent the law allows, OpenCPA and Hayden Harms aren’t liable for any
        indirect, incidental, special or consequential damages, or for exam results, lost data or
        lost opportunities, arising from your use of the site. Because the site is free, total
        liability for any claim is limited to $0, or the smallest amount the law permits.
      </p>

      <h2>Changes and governing law</h2>
      <p>
        We may update these terms; the date at the top shows the latest version, and continuing to
        use the site means you accept it. These terms are governed by the laws of the State of
        Texas.
      </p>

      <h2>Contact</h2>
      <p>
        Questions: open an issue at <a href={ISSUES}>github.com/HaydenHarms/opencpa/issues</a>. See
        also the <Link to="/privacy">Privacy Policy</Link>.
      </p>
    </section>
  );
}
