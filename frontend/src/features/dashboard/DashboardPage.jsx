import { useEffect, useState } from "react";
import { AlertTriangle, Bird, DollarSign, Egg, HeartPulse, Home, Syringe, Wheat } from "lucide-react";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Link } from "react-router-dom";
import PageHeader from "../../components/ui/PageHeader";
import { ErrorState, LoadingScreen } from "../../components/ui/Feedback";
import { api, apiError } from "../../lib/api";

const money = (value) => `KES ${Number(value || 0).toLocaleString()}`;
function Metric({ label, value, Icon, tone = "farm" }) {
  const colors = tone === "red" ? "bg-red-50 text-red-700" : tone === "amber" ? "bg-amber-50 text-amber-700" : "bg-farm-50 text-farm-700";
  return <article className="card p-4 sm:p-5"><div className="flex items-center justify-between"><div><p className="text-sm text-stone-500">{label}</p><p className="mt-2 text-2xl font-bold">{value}</p></div><span className={`rounded-2xl p-3 ${colors}`}><Icon /></span></div></article>;
}

export default function DashboardPage() {
  const [data, setData] = useState(null); const [error, setError] = useState("");
  const load = () => { setError(""); api.get("/dashboard/").then((r) => setData(r.data)).catch((e) => setError(apiError(e))); };
  useEffect(load, []);
  if (!data && !error) return <LoadingScreen />;
  if (error) return <ErrorState message={error} retry={load} />;
  const metrics = [["Total birds", data.total_birds, Bird], ["Active houses", data.active_poultry_houses, Home], ["Eggs today", data.eggs_collected_today, Egg], ["Feed stock", `${data.feed_stock_kg} kg`, Wheat], ["Mortality today", data.mortality_today, HeartPulse, "red"], ["Vaccinations due", data.upcoming_vaccinations, Syringe, "amber"]];
  return <><PageHeader title="Farm dashboard" description={`A clear view of today’s farm operations.`} />
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">{metrics.map(([label, value, Icon, tone]) => <Metric key={label} {...{ label, value, Icon, tone }} />)}</section>
    {data.financials && <section className="mt-4 grid gap-4 sm:grid-cols-3"><Metric label="Sales this month" value={money(data.financials.sales_this_month)} Icon={DollarSign} /><Metric label="Expenses this month" value={money(data.financials.expenses_this_month)} Icon={DollarSign} tone="amber" /><Metric label="Profit this month" value={money(data.financials.profit_this_month)} Icon={DollarSign} tone={Number(data.financials.profit_this_month) < 0 ? "red" : "farm"} /></section>}
    <section className="mt-6 grid gap-5 xl:grid-cols-2"><article className="card p-4 sm:p-6"><h2 className="font-bold">Egg production — 30 days</h2><div className="mt-5 h-64"><ResponsiveContainer width="100%" height="100%"><AreaChart data={data.production_chart}><defs><linearGradient id="eggs" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#2f8550" stopOpacity={0.35}/><stop offset="95%" stopColor="#2f8550" stopOpacity={0}/></linearGradient></defs><CartesianGrid strokeDasharray="3 3" vertical={false}/><XAxis dataKey="record_date" tick={{ fontSize: 11 }}/><YAxis width={40}/><Tooltip/><Area type="monotone" dataKey="eggs" stroke="#257044" fill="url(#eggs)" strokeWidth={2}/></AreaChart></ResponsiveContainer></div></article>
      {data.financials && <article className="card p-4 sm:p-6"><h2 className="font-bold">Sales — 30 days</h2><div className="mt-5 h-64"><ResponsiveContainer width="100%" height="100%"><BarChart data={data.sales_chart}><CartesianGrid strokeDasharray="3 3" vertical={false}/><XAxis dataKey="day" tick={{ fontSize: 11 }}/><YAxis width={50}/><Tooltip formatter={(v) => money(v)}/><Bar dataKey="amount" fill="#2f8550" radius={[6,6,0,0]}/></BarChart></ResponsiveContainer></div></article>}</section>
    <section className="mt-6 grid gap-5 xl:grid-cols-[1fr_1.5fr]"><article className="card p-5"><h2 className="font-bold">Quick actions</h2><div className="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-1">{data.quick_actions.map((action) => <Link key={action.key} to={action.path} className="flex min-h-12 items-center justify-between rounded-xl border px-4 font-semibold hover:border-farm-300 hover:bg-farm-50">{action.label}<span>→</span></Link>)}</div></article>
      <article className="card overflow-hidden"><div className="border-b p-5"><h2 className="font-bold">Birds by batch</h2></div><div className="divide-y">{data.birds_by_batch.map((batch) => <div key={batch.id} className="flex items-center justify-between p-4"><div><strong>{batch.batch_code}</strong><p className="text-sm text-stone-500">{batch.batch_name}</p></div><span className="rounded-full bg-farm-50 px-3 py-1 font-bold text-farm-700">{batch.current_bird_count.toLocaleString()}</span></div>)}{!data.birds_by_batch.length && <div className="p-8 text-center text-stone-500"><AlertTriangle className="mx-auto mb-2"/>No active batches</div>}</div></article></section>
  </>;
}

