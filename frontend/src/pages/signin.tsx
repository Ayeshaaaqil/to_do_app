// frontend/src/pages/signin.tsx

import React from 'react';
import SigninForm from '../components/auth/SigninForm';
import Layout from '../components/layout/Layout';

const SigninPage: React.FC = () => {
  return (
    <Layout>
      <div className="min-h-screen flex items-center justify-center py-12">
        <div className="max-w-4xl w-full flex flex-col md:flex-row rounded-2xl overflow-hidden shadow-xl">
          {/* Left side with illustration */}
          <div className="md:w-1/2 bg-gradient-to-br from-indigo-500 to-purple-600 p-8 flex flex-col justify-center">
            <div className="text-white text-center">
              <h1 className="text-3xl font-bold mb-4 font-poppins">Welcome Back!</h1>
              <p className="text-lg mb-6">Sign in to access your productivity dashboard</p>
              <div className="bg-white/20 backdrop-blur-sm rounded-xl p-6">
                <img
                  src="https://www.shutterstock.com/image-vector/set-sign-forms-colorful-gradient-260nw-2082628327.jpg"
                  alt="Productivity illustration"
                  className="w-full rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* Right side with form */}
          <div className="md:w-1/2 bg-white dark:bg-gray-800 p-8 flex flex-col justify-center">
            <div className="max-w-md mx-auto w-full">
              <div className="text-center mb-8">
                <h2 className="text-2xl font-bold text-gray-800 dark:text-white">Sign In to TodoPro</h2>
                <p className="text-gray-600 dark:text-gray-300 mt-2">Manage your tasks efficiently</p>
              </div>
              <SigninForm />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default SigninPage;