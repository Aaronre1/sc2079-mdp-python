import "@/styles/globals.css";
import Head from "next/head";
import Simulator from "components/Simulator";

export default function App({ Component, pageProps }) {
  return (
    <div className="bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-teal-100 via-teal-200 to-teal-200 h-screen overflow-auto">
      <Head>
        <title>MDP Simulator</title>
      </Head>
      <Simulator />
    </div>
  );
}
