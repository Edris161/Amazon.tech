"use client"

import { useState } from "react"

export default function LoginPage() {
  const [form, setForm] = useState({
    username: "",
    password: ""
  })

  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: any) => {
    e.preventDefault()

    const res = await fetch("http://127.0.0.1:8000/api/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    })

    const data = await res.json()

    if (res.ok) {
      localStorage.setItem("token", data.access)
      alert("You successfully logged in 🎉")
    } else {
      alert("Invalid credentials")
    }
  }

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input name="username" placeholder="Username" onChange={handleChange} className="border p-2" />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} className="border p-2" />
        <button className="bg-green-500 text-white px-4 py-2">Login</button>
      </form>
    </div>
  )
}
