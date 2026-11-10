export default function Navbar({ page, onPage }) {
  return (
    <header className="topbar">
      <a
        className="brand"
        href="#"
        onClick={(e) => {
          e.preventDefault();
          onPage("classify");
        }}
      >
        <span className="brand-icon" aria-hidden="true">
          ✿
        </span>
        <span>
          iris<span className="brand-sub">BOTANICAL INTELLIGENCE</span>
        </span>
      </a>
      <nav aria-label="Main navigation">
        <button
          className={page === "classify" ? "active" : ""}
          onClick={() => onPage("classify")}
        >
          Classify flower
        </button>
        <button
          className={page === "performance" ? "active" : ""}
          onClick={() => onPage("performance")}
        >
          Model performance
        </button>
      </nav>
      <span className="desktop-note">DECISION TREE / v1.0</span>
    </header>
  );
}
