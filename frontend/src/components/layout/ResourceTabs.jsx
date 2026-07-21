import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import PageHeader from "../ui/PageHeader";

export default function ResourceTabs({ title, description, tabs }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialTab = tabs.findIndex((tab) => tab.label.toLowerCase() === searchParams.get("tab")?.toLowerCase());
  const [active, setActive] = useState(initialTab >= 0 ? initialTab : 0);
  useEffect(() => {
    const tabParam = searchParams.get("tab");
    if (!tabParam) return;
    const nextIndex = tabs.findIndex((tab) => tab.label.toLowerCase() === tabParam.toLowerCase());
    if (nextIndex >= 0) setActive(nextIndex);
  }, [searchParams, tabs]);
  const Current = tabs[active].component;
  const choose = (index) => {
    setActive(index);
    const next = new URLSearchParams(searchParams);
    next.set("tab", tabs[index].label);
    setSearchParams(next, { replace: true });
  };
  return <div><PageHeader title={title} description={description} /><div className="mb-5 flex gap-2 overflow-x-auto pb-1">{tabs.map((tab, index) => <button key={tab.label} onClick={() => choose(index)} className={`min-h-10 whitespace-nowrap rounded-xl px-4 text-sm font-semibold ${active === index ? "bg-farm-600 text-white" : "border bg-white text-stone-600"}`}>{tab.label}</button>)}</div><Current embedded /></div>;
}
