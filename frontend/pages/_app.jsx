import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  return (
    <div id="main-container">
      <nav className="bg-sky-500 text-white p-5">
        <a href="/">
          <h1 className="text-3xl">Movie Recommendation Engine</h1>
        </a>
      </nav>
      <Component {...pageProps} />
    </div>
  );
}

export default MyApp;
