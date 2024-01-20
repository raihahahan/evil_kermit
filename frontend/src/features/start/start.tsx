import { useState } from "react";
import Image from "next/image";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

function getInstructionalText(responded: boolean): string {
  return !responded
    ? "Step 1: Fill in your phone number (with country code)"
    : "Step 2: Fill in your OTP";
}

export default function Start() {
  const [formState, setFormState] = useState({
    responded: false,
    inputValue: "",
    usernameValue: "",
    whitelistedContactsValue: "",
    passwordValue: "",
    passwordDisabled: true,
  });

  const [loading, setLoading] = useState(false);

  const handleInputChange =
    (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
      setFormState({
        ...formState,
        [field]: event.target.value,
      });
    };

  const handleSubmitFirstStep = async () => {
    setLoading(true);
    setTimeout(() => {
      setFormState({
        ...formState,
        responded: true,
        passwordDisabled: false,
      });
      setLoading(false);
    }, 3000);
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormState({
      ...formState,
      passwordValue: event.target.value,
    });
  };

  const handleSubmitSecondStep = () => {
    console.log("Password form submitted");
  };

  return (
    <main
      className={`flex h-screen w-screen flex-col items-center justify-center p-24 ${inter.className}`}
    >
      <div className="mb-32 grid text-center w-1/2 h-1/2">
        <div className="w-full h-full group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className={`mb-3 text-2xl font-semibold`}>
            {getInstructionalText(formState.responded)}
          </h2>
          <form
            onSubmit={e => {
              e.preventDefault();
              handleSubmitFirstStep();
            }}
            className="grid grid-cols-2 gap-4 w-full"
          >
            <div className="flex flex-col items-start">
              <label
                htmlFor="phoneNumber"
                className="mb-1 text-base font-semibold"
              >
                Phone Number
              </label>
              <input
                type="text"
                id="phoneNumber"
                value={formState.inputValue}
                onChange={handleInputChange("inputValue")}
                disabled={formState.responded}
                className="p-2 border border-gray-300 w-full"
                title="Phone Number"
                placeholder="(e.g. +6512345678)"
              />
            </div>

            <div className="flex flex-col items-start">
              <label
                htmlFor="username"
                className="mb-1 text-base font-semibold"
              >
                Username
              </label>
              <input
                type="text"
                id="username"
                value={formState.usernameValue}
                onChange={handleInputChange("usernameValue")}
                disabled={formState.responded}
                className="p-2 border border-gray-300 w-full"
                title="Username"
                placeholder="Enter your username"
              />
            </div>

            {formState.responded && (
              <div className="flex flex-col items-start col-span-2">
                <label
                  htmlFor="password"
                  className="mb-1 text-base font-semibold"
                >
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={formState.passwordValue}
                  onChange={handlePasswordChange}
                  disabled={formState.passwordDisabled}
                  className="p-2 border border-gray-300 w-full"
                />
              </div>
            )}

            <div className="flex flex-col items-start">
              <label
                htmlFor="whitelistedContacts"
                className="mb-1 text-base font-semibold"
              >
                Whitelisted Contacts
              </label>
              <input
                type="text"
                id="whitelistedContacts"
                value={formState.whitelistedContactsValue}
                onChange={handleInputChange("whitelistedContactsValue")}
                disabled={formState.responded}
                className="p-2 border border-gray-300 w-full"
                title="Whitelisted Contacts"
                placeholder="Enter whitelisted contacts"
              />
            </div>

            <button
              type="submit"
              className="col-span-2 m-2 p-2 bg-blue-500 text-white relative"
              disabled={formState.responded}
            >
              {loading ? (
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V2.83A10 10 0 002.83 12H4zm2 0a5.96 5.96 0 014.22-5.72A8 8 0 014 12H6zm2 0a5.96 5.96 0 014.22 5.72 8 8 0 01-4.22-5.72H8zm2 0a2.98 2.98 0 011.76 5.44A8 8 0 018 12h2zm5.66-1.72a5.96 5.96 0 01-4.22 5.72 8 8 0 014.22-5.72z"
                  ></path>
                </svg>
              ) : (
                "Submit"
              )}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
