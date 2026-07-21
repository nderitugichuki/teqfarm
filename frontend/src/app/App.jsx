import { Route, Routes } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import ProfilePage from "../features/auth/ProfilePage";
import LoginPage from "../features/auth/LoginPage";
import DashboardPage from "../features/dashboard/DashboardPage";
import NotificationsPage from "../features/notifications/NotificationsPage";
import ReportsPage from "../features/reports/ReportsPage";
import NotFoundPage from "../pages/NotFoundPage";
import { DailyRecordsPage, EggsPage, ExpensesPage, FeedPage, FlocksPage, HealthPage, HousesPage, InventoryPage, SalesPage } from "../pages/Resources";
import ProtectedRoute from "./ProtectedRoute";

const managementRoles = ["administrator", "manager"];
const protectedLayout = <ProtectedRoute><AppLayout /></ProtectedRoute>;

export default function App() {
  return <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route element={protectedLayout}>
      <Route index element={<DashboardPage />} />
      <Route path="daily-records" element={<DailyRecordsPage />} />
      <Route path="houses" element={<HousesPage />} />
      <Route path="flocks" element={<FlocksPage />} />
      <Route path="feed" element={<FeedPage />} />
      <Route path="eggs" element={<EggsPage />} />
      <Route path="health" element={<HealthPage />} />
      <Route path="inventory" element={<InventoryPage />} />
      <Route path="notifications" element={<NotificationsPage />} />
      <Route path="profile" element={<ProfilePage />} />
      <Route path="sales" element={<ProtectedRoute roles={managementRoles}><SalesPage /></ProtectedRoute>} />
      <Route path="expenses" element={<ProtectedRoute roles={managementRoles}><ExpensesPage /></ProtectedRoute>} />
      <Route path="reports" element={<ProtectedRoute roles={managementRoles}><ReportsPage /></ProtectedRoute>} />
      <Route path="*" element={<NotFoundPage />} />
    </Route>
  </Routes>;
}

