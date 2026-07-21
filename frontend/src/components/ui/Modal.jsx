import { X } from "lucide-react";
import { useEffect } from "react";

export default function Modal({ open, title, children, onClose }) {
  useEffect(() => {
    if (!open) return undefined;
    const escape = (event) => event.key === "Escape" && onClose();
    document.addEventListener("keydown", escape); document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", escape); document.body.style.overflow = ""; };
  }, [open, onClose]);
  if (!open) return null;
  return <div className="fixed inset-0 z-[70] grid items-end sm:place-items-center"><button aria-label="Close dialog" onClick={onClose} className="absolute inset-0 bg-black/45" />
    <section role="dialog" aria-modal="true" className="relative max-h-[92vh] w-full overflow-y-auto rounded-t-3xl bg-white p-5 shadow-2xl sm:max-w-2xl sm:rounded-3xl sm:p-7">
      <header className="mb-5 flex items-center justify-between"><h2 className="text-xl font-bold">{title}</h2><button onClick={onClose} className="rounded-lg p-2 hover:bg-stone-100"><X /></button></header>{children}</section></div>;
}

