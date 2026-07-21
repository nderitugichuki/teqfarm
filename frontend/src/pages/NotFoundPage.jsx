import { Link } from "react-router-dom";
export default function NotFoundPage() { return <div className="grid min-h-[70vh] place-items-center text-center"><div><p className="text-7xl font-black text-farm-200">404</p><h1 className="mt-3 text-2xl font-bold">That page wandered off</h1><p className="mt-2 text-stone-500">Let’s get you back to the farm.</p><Link className="btn-primary mt-6" to="/">Go to dashboard</Link></div></div>; }

