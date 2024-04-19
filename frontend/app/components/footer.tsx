import Image from "next/image";

const Footer = () => {
  return (
    <div className="w-full pt-2 items-center justify-between font-mono text-sm lg:flex">
      <p className="">
        Develovep by&nbsp;
        <a href="" target="_blank" className="font-mono font-bold">Blazzbyte</a>
      </p>
      <div className="">
        <a
          href="https://www.llamaindex.ai/"
          target="_blank"
          className="flex items-center justify-center font-nunito text-lg font-bold gap-2"
        >
          <span>Built with LlamaIndex</span>
          <Image
            className="rounded-xl"
            src="/llama.png"
            alt="Llama Logo"
            width={35}
            height={35}
            priority
          />
        </a>
      </div>
    </div>
  )
}

export default Footer