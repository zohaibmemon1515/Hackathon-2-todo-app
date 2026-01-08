import Link from 'next/link';
import Navigation from '../ui/navigation';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-indigo-600">
              Todo App
            </Link>
          </div>
          <nav className="hidden md:flex space-x-8">
            <Link
              href="/dashboard"
              className="text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Dashboard
            </Link>
            <Link
              href="/features"
              className="text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Features
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <Link
              href="/auth/login"
              className="text-sm font-medium text-gray-500 hover:text-gray-900"
            >
              Sign in
            </Link>
            <Link
              href="/auth/register"
              className="text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-md"
            >
              Sign up
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}