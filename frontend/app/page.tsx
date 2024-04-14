import Header from "@/app/components/header";
import Sidebar from "@/app/components/sidebar";
import Footer from "@/app/components/footer";

import ChatSection from "./components/chat-section";

export default function Home() {
  return (
    <main className="h-full flex gap-4 p-24 background-gradient">
      <Sidebar />
      <section className="w-9/12 flex flex-col">
        <ChatSection />
        <Footer />
      </section>
    </main>
  );
}
