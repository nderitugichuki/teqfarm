import { useState } from "react";
import { KeyRound, LoaderCircle, Save } from "lucide-react";
import { toast } from "sonner";
import PageHeader from "../../components/ui/PageHeader";
import { api, apiError } from "../../lib/api";
import { useAuth } from "./AuthContext";

export default function ProfilePage() {
  const { user, setUser, logout } = useAuth();
  const [profile, setProfile] = useState({ first_name: user.first_name || "", last_name: user.last_name || "", email: user.email || "", phone_number: user.phone_number || "", job_title: user.job_title || "" });
  const [password, setPassword] = useState({ current_password: "", new_password: "", confirm_password: "" });
  const [saving, setSaving] = useState("");
  async function saveProfile(e) { e.preventDefault(); setSaving("profile"); try { const { data } = await api.patch("/auth/profile/", profile); setUser(data); localStorage.setItem("teqfarm_user", JSON.stringify(data)); toast.success("Profile updated."); } catch (err) { toast.error(apiError(err)); } finally { setSaving(""); } }
  async function changePassword(e) { e.preventDefault(); setSaving("password"); try { await api.post("/auth/change-password/", password); toast.success("Password changed. Please sign in again."); await logout(); } catch (err) { toast.error(apiError(err)); } finally { setSaving(""); } }
  return <><PageHeader title="Your profile" description={`${user.username} · ${user.role}`} /><div className="grid gap-6 xl:grid-cols-2"><form onSubmit={saveProfile} className="card space-y-4 p-5 sm:p-6"><h2 className="text-lg font-bold">Personal details</h2><div className="grid gap-4 sm:grid-cols-2">{[["first_name", "First name"], ["last_name", "Last name"], ["email", "Email", "email"], ["phone_number", "Phone"], ["job_title", "Job title"]].map(([key, label, type]) => <label key={key}><span className="label">{label}</span><input type={type || "text"} className="field" value={profile[key]} onChange={(e) => setProfile({ ...profile, [key]: e.target.value })} /></label>)}</div><button className="btn-primary" disabled={saving === "profile"}>{saving === "profile" ? <LoaderCircle className="animate-spin" /> : <Save />}Save profile</button></form>
    <form onSubmit={changePassword} className="card space-y-4 p-5 sm:p-6"><h2 className="flex items-center gap-2 text-lg font-bold"><KeyRound />Change password</h2>{[["current_password", "Current password"], ["new_password", "New password"], ["confirm_password", "Confirm new password"]].map(([key, label]) => <label key={key}><span className="label">{label}</span><input required type="password" className="field" value={password[key]} onChange={(e) => setPassword({ ...password, [key]: e.target.value })} /></label>)}<button className="btn-primary" disabled={saving === "password"}>{saving === "password" && <LoaderCircle className="animate-spin" />}Change password</button></form></div></>;
}

