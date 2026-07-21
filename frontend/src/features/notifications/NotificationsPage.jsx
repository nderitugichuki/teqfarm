import { useEffect, useState } from "react";
import { AlertTriangle, Bell, CheckCheck, CircleAlert, Info } from "lucide-react";
import { toast } from "sonner";
import PageHeader from "../../components/ui/PageHeader";
import { EmptyState, ErrorState, LoadingScreen } from "../../components/ui/Feedback";
import { api, apiError, results } from "../../lib/api";

const icons = { critical: CircleAlert, warning: AlertTriangle, info: Info };
export default function NotificationsPage() {
  const [items, setItems] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState("");
  const load = () => { setLoading(true); api.get("/notifications/", { params: { page_size: 100 } }).then(({ data }) => setItems(results(data))).catch((e) => setError(apiError(e))).finally(() => setLoading(false)); };
  useEffect(load, []);
  async function read(item) { if (item.is_read) return; await api.post(`/notifications/${item.id}/read/`); setItems(items.map((x) => x.id === item.id ? { ...x, is_read: true } : x)); }
  async function readAll() { try { await api.post("/notifications/read-all/"); setItems(items.map((x) => ({ ...x, is_read: true }))); toast.success("All alerts marked as read."); } catch (e) { toast.error(apiError(e)); } }
  return <><PageHeader title="Notifications" description="Farm conditions that need attention." actions={<button onClick={readAll} className="btn-secondary"><CheckCheck />Mark all read</button>} />
    {loading ? <LoadingScreen /> : error ? <ErrorState message={error} retry={load} /> : !items.length ? <EmptyState message="No alerts right now. The farm is looking tidy." /> : <div className="space-y-3">{items.map((item) => { const Icon = icons[item.severity] || Bell; return <button key={item.id} onClick={() => read(item)} className={`card flex w-full gap-4 p-4 text-left sm:p-5 ${item.is_resolved ? "opacity-55" : ""}`}><span className={`rounded-xl p-2.5 ${item.severity === "critical" ? "bg-red-50 text-red-700" : item.severity === "warning" ? "bg-amber-50 text-amber-700" : "bg-blue-50 text-blue-700"}`}><Icon /></span><span className="min-w-0 flex-1"><span className="flex items-start justify-between gap-3"><strong>{item.title}</strong>{!item.is_read && <span className="mt-1 h-2.5 w-2.5 shrink-0 rounded-full bg-farm-500" />}</span><span className="mt-1 block text-sm text-stone-600">{item.message}</span><small className="mt-2 block text-stone-400">{item.due_date || new Date(item.created_at).toLocaleDateString()}{item.is_resolved && " · Resolved"}</small></span></button>; })}</div>}
  </>;
}
