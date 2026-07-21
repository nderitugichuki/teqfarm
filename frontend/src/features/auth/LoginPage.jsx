import { useState } from "react";
import { Bird, LoaderCircle, LockKeyhole, User } from "lucide-react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { apiError } from "../../lib/api";
import { useAuth } from "./AuthContext";

export default function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ username: "", password: "" });
  if (user) return <Navigate to="/" replace />;

  async function submit(event) {
    event.preventDefault(); setLoading(true);
    try { await login(form); navigate(location.state?.from || "/", { replace: true }); }
    catch (error) { toast.error(apiError(error)); }
    finally { setLoading(false); }
  }

  return <main className="grid min-h-screen lg:grid-cols-2">
    <section className="hidden bg-farm-900 p-12 text-white lg:flex lg:flex-col lg:justify-between">
      <div className="flex items-center gap-3 text-2xl font-bold"><Bird className="h-9 w-9" />TeqFarm</div>
      <div><p className="max-w-lg text-4xl font-bold leading-tight">Every flock, every egg, every shilling—clearly managed.</p>
        <p className="mt-5 max-w-md text-farm-100">A practical poultry operations system built for work in the office and inside the poultry house.</p></div>
      <p className="text-sm text-farm-100">Secure farm operations</p>
    </section>
    <section className="flex items-center justify-center p-5 sm:p-10">
      <form onSubmit={submit} className="w-full max-w-md space-y-6">
        <div className="lg:hidden flex items-center gap-2 text-2xl font-bold text-farm-700"><Bird />TeqFarm</div>
        <div><h1 className="text-3xl font-bold">Welcome back</h1><p className="mt-2 text-stone-500">Sign in to manage the farm.</p></div>
        <label><span className="label">Username</span><div className="relative"><User className="absolute left-3 top-3 h-5 w-5 text-stone-400" />
          <input className="field pl-10" autoComplete="username" required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} /></div></label>
        <label><span className="label">Password</span><div className="relative"><LockKeyhole className="absolute left-3 top-3 h-5 w-5 text-stone-400" />
          <input className="field pl-10" type="password" autoComplete="current-password" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></div></label>
        <button className="btn-primary w-full" disabled={loading}>{loading && <LoaderCircle className="animate-spin" />}Sign in</button>
      </form>
    </section>
  </main>;
}

