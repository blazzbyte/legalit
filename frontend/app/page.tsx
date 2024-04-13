import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";
import Footer from "./components/footer";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-4 p-24 background-gradient">
      <Header />
      <ChatSection />
      <Footer />
    </main>
  );
}
