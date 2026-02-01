"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";
import { FaGithub } from "react-icons/fa";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/components/providers/AuthProvider";

export default function Home() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-gray-950 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* Navigation */}
      <nav className="flex items-center justify-between px-6 py-6 border-b border-gray-100 dark:border-gray-900 sticky top-0 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md z-50">
        <div className="flex items-center gap-2 group cursor-pointer">
          <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-200 dark:shadow-none group-hover:scale-110 transition-transform duration-300">
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
            Mantis Bot
          </span>
        </div>
        <div className="flex items-center gap-4">
          <Link
            href="https://github.com"
            className="text-gray-500 hover:text-gray-900 dark:hover:text-white transition-colors p-2"
          >
            <FaGithub size={24} />
          </Link>
          <Button
            asChild
            variant="ghost"
            className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 font-medium"
          >
            <Link href={isAuthenticated ? "/dashboard" : "/login"}>
              {isAuthenticated ? "Dashboard" : "Sign In"}
            </Link>
          </Button>
          {!isAuthenticated && (
            <Button
              asChild
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 rounded-lg shadow-lg shadow-indigo-100 dark:shadow-none hover:-translate-y-0.5 transition-all duration-200"
            >
              <Link href="/login">Get Started</Link>
            </Button>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-grow">
        <section className="relative px-6 pt-24 pb-32 overflow-hidden">
          {/* Background Decorative Elements */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-full -z-10 opacity-50">
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-50 dark:bg-indigo-900/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-purple-50 dark:bg-purple-900/10 rounded-full blur-3xl" />
          </div>

          <div className="max-w-5xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-400 rounded-full text-sm font-semibold border border-indigo-100 dark:border-indigo-900/30">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
              </span>
              v1.0 is now live
            </div>

            <h1 className="text-6xl md:text-7xl font-extrabold tracking-tight text-gray-900 dark:text-white leading-[1.1]">
              Automate Your
              <span className="block text-indigo-600 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                Customer Support
              </span>
            </h1>

            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto leading-relaxed">
              Deploy intelligent chatbots in minutes. Leverage cutting-edge AI
              to handle inquiries, resolve issues, and delight customers 24/7.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Button
                asChild
                size="lg"
                className="w-full sm:w-auto px-8 bg-indigo-600 hover:bg-indigo-700 text-white text-lg font-bold rounded-xl shadow-xl shadow-indigo-200 dark:shadow-none transition-all duration-300 transform hover:scale-105"
              >
                <Link href="/login">Start Free Trial</Link>
              </Button>
              <Button
                asChild
                variant="outline"
                size="lg"
                className="w-full sm:w-auto px-8 py-6 border-2 border-gray-200 dark:border-gray-800 text-lg font-bold rounded-xl hover:bg-gray-50 dark:hover:bg-gray-900 transition-all duration-300"
              >
                <Link href="#features">View Demo</Link>
              </Button>
            </div>

            {/* Trusted By Section or Feature Badges */}
            <div className="pt-20 grid grid-cols-2 md:grid-cols-4 gap-8">
              {[
                { label: "Uptime", value: "99.9%" },
                { label: "Latency", value: "<50ms" },
                { label: "Accuracy", value: "98.5%" },
                { label: "ROI", value: "2.4x" },
              ].map((stat, i) => (
                <div key={i} className="space-y-1">
                  <div className="text-3xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </div>
                  <div className="text-sm font-medium text-gray-500 dark:text-gray-400">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Preview Badge */}
        <section id="features" className="py-24 bg-gray-50 dark:bg-gray-900/50">
          <div className="max-w-7xl mx-auto px-6">
            <div className="flex flex-wrap items-center justify-center gap-6">
              {[
                "Multi-tenancy",
                "Keycloak OAuth",
                "Real-time Analytics",
                "Advanced LLMs",
              ].map((feature, i) => (
                <Badge
                  key={i}
                  variant="secondary"
                  className="px-4 py-2 text-sm bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 shadow-sm"
                >
                  {feature}
                </Badge>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="py-12 px-6 border-t border-gray-100 dark:border-gray-900 bg-white dark:bg-gray-950">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gray-900 dark:bg-white rounded-lg flex items-center justify-center text-white dark:text-gray-950">
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <span className="font-bold text-gray-900 dark:text-white">
              Mantis Bot
            </span>
          </div>
          <p className="text-gray-500 text-sm">
            © 2024 Mantis Bot. Built for the modern enterprise.
          </p>
          <div className="flex gap-6">
            <Link
              href="#"
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-sm"
            >
              Privacy
            </Link>
            <Link
              href="#"
              className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-sm"
            >
              Terms
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
