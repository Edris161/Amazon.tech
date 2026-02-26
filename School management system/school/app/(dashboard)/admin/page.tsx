export default function AdminDashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>

      <div className="grid grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow">
          <h2>Total Students</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h2>Total Teachers</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h2>Total Classes</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow">
          <h2>Total Revenue</h2>
          <p className="text-3xl font-bold">$0</p>
        </div>
      </div>
    </div>
  );
}