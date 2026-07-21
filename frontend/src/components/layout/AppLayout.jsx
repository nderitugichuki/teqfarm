import { useEffect, useState } from "react";
import { Bell, Bird, ChevronDown, ClipboardList, DollarSign, Egg, HeartPulse, Home, Menu, Package, PanelLeftClose, ReceiptText, ScrollText, Settings, TrendingUp, Warehouse, Wheat, X } from "lucide-react";
import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthContext";
import { api, results } from "../../lib/api";

const nav = [
  ["Dashboard", "/", Home], ["Daily records", "/daily-records", ClipboardList],
  ["Poultry houses", "/houses", Warehouse], ["Flocks", "/flocks", Bird],
  ["Feed", "/feed", Wheat], ["Eggs", "/eggs", Egg],
  ["Health", "/health", HeartPulse], ["Inventory", "/inventory", Package],
  ["Sales", "/sales", TrendingUp, true], ["Expenses", "/expenses", DollarSign, true],
  ["Reports", "/reports", ScrollText, true], ["Notifications", "/notifications", Bell],
];

function NavItems({ close, canManage }) {
  return <nav className="space-y-1">{nav.filter((item) => !item[3] || canManage).map(([label, path, Icon]) =>
    <NavLink key={path} to={path} end={path === "/"} onClick={close} className={({ isActive }) =>
      `flex min-h-11 items-center gap-3 rounded-xl px-3 text-sm font-semibold transition ${isActive ? "bg-farm-100 text-farm-800" : "text-stone-600 hover:bg-stone-100"}`}>
      <Icon className="h-5 w-5" />{label}</NavLink>)}</nav>;
}

export default function AppLayout() {
  const { user, logout, canManage } = useAuth();
  const [drawer, setDrawer] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [unread, setUnread] = useState(0);
  const location = useLocation();
  useEffect(() => { setDrawer(false); }, [location.pathname]);
  useEffect(() => {
    api.get("/notifications/", { params: { is_resolved: false, page_size: 100 } })
      .then(({ data }) => setUnread(results(data).filter((n) => !n.is_read).length)).catch(() => {});
  }, [location.pathname]);

  return <div className="min-h-screen lg:flex">
    <aside className={`hidden border-r bg-white p-4 lg:fixed lg:inset-y-0 lg:flex lg:flex-col ${collapsed ? "lg:w-20" : "lg:w-64"}`}>
      <div className="mb-7 flex items-center justify-between px-2"><span className="flex items-center gap-2 text-xl font-bold text-farm-700"><Bird />{!collapsed && "TeqFarm"}</span>
        <button aria-label="Collapse navigation" onClick={() => setCollapsed(!collapsed)} className="rounded-lg p-2 hover:bg-stone-100"><PanelLeftClose className={collapsed ? "rotate-180" : ""} /></button></div>
      <div className={collapsed ? "[&_a]:justify-center [&_a]:text-0 [&_a_svg]:h-5" : ""}><NavItems canManage={canManage} /></div>
      <div className="mt-auto border-t pt-4"><NavLink to="/profile" className="flex items-center gap-3 rounded-xl p-2 hover:bg-stone-50">
        <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-farm-100 font-bold text-farm-700">{user?.first_name?.[0] || user?.username?.[0]?.toUpperCase()}</span>
        {!collapsed && <span className="min-w-0"><strong className="block truncate text-sm">{user?.full_name || user?.username}</strong><small className="capitalize text-stone-500">{user?.role}</small></span>}</NavLink></div>
    </aside>

    {drawer && <div className="fixed inset-0 z-50 lg:hidden"><button aria-label="Close menu" className="absolute inset-0 bg-black/40" onClick={() => setDrawer(false)} />
      <aside className="relative h-full w-[86%] max-w-xs overflow-y-auto bg-white p-5 shadow-xl"><div className="mb-6 flex items-center justify-between"><span className="flex items-center gap-2 text-xl font-bold text-farm-700"><Bird />TeqFarm</span><button onClick={() => setDrawer(false)}><X /></button></div><NavItems canManage={canManage} close={() => setDrawer(false)} /></aside></div>}

    <div className={`min-w-0 flex-1 ${collapsed ? "lg:ml-20" : "lg:ml-64"}`}>
      <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-white/95 px-4 backdrop-blur sm:px-6">
        <button className="rounded-lg p-2 lg:hidden" onClick={() => setDrawer(true)} aria-label="Open menu"><Menu /></button>
        <div className="hidden lg:block"><p className="text-sm text-stone-500">TeqFarm operations</p></div>
        <div className="flex items-center gap-2"><NavLink to="/notifications" className="relative rounded-xl p-2.5 hover:bg-stone-100"><Bell />{unread > 0 && <span className="absolute right-1 top-1 h-2.5 w-2.5 rounded-full bg-red-500 ring-2 ring-white" />}</NavLink>
          <button onClick={logout} className="hidden min-h-10 items-center gap-2 rounded-xl px-3 text-sm font-semibold hover:bg-stone-100 sm:flex">Sign out<ChevronDown className="h-4 w-4" /></button></div>
      </header>
      <main className="mx-auto max-w-[1600px] p-4 pb-24 sm:p-6 lg:p-8 lg:pb-8"><Outlet /></main>
    </div>
    <nav className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-5 border-t bg-white px-1 pb-[env(safe-area-inset-bottom)] lg:hidden">
      {[["Home", "/", Home], ["Record", "/daily-records", ClipboardList], ["Flocks", "/flocks", Bird], ["Sales", canManage ? "/sales" : "/eggs", ReceiptText], ["More", "/profile", Settings]].map(([label, path, Icon]) =>
        <NavLink key={label} to={path} className={({ isActive }) => `flex min-h-16 flex-col items-center justify-center gap-1 text-[11px] font-semibold ${isActive ? "text-farm-700" : "text-stone-500"}`}><Icon className="h-5 w-5" />{label}</NavLink>)}</nav>
  </div>;
}

