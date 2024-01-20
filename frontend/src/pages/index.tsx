import { useState } from "react";
import Image from "next/image";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

function getInstructionalText(responded: boolean): string {
  return !responded
    ? "Step 1: Fill in your phone number (with country code)"
    : "Step 2: Fill in your OTP";
}

export default function Home() {
  const [formState, setFormState] = useState({
    responded: false,
    inputValue: "",
    passwordValue: "",
    passwordDisabled: true,
  });

  const [loading, setLoading] = useState(false);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormState({
      ...formState,
      inputValue: event.target.value,
    });
  };

  const handleSubmitFirstStep = async () => {
    // Your async function logic goes here
    setLoading(true);
    setTimeout(() => {
      setFormState({
        ...formState,
        responded: true,
        passwordDisabled: false,
      });
    }, 3000);

    // Assuming the async function has completed successfully
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormState({
      ...formState,
      passwordValue: event.target.value,
    });
  };

  const handleSubmitSecondStep = () => {
    // Your password form submission logic goes here
    console.log("Password form submitted");
  };

  return (
    <main
      className={`flex h-screen w-screen flex-col items-center justify-center p-24 ${inter.className}`}
    >
      <div className="mb-32 grid text-center w-1/2 h-1/2">
        <div className="w-full h-full group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className={`mb-3 text-2xl font-semibold`}>
            {/* {getInstructionalText(formState.responded)} */}
            Step 1: Phone Number
          </h2>
          {/* <h2 className={`mb-3 text-2xl font-semibold`}>
            {getInstructionalText(formState.responded)}
          </h2> */}
          <h6 className={`mb-3 text-m`}>
            Fill in your phone number (with country code)
          </h6>
          {/* {loading ? "nothing", } */}

          <form
            onSubmit={e => {
              e.preventDefault();
              handleSubmitFirstStep();
            }}
            className="flex flex-col items-center"
          >
            <input
              type="text"
              value={formState.inputValue}
              onChange={handleInputChange}
              disabled={formState.responded}
              className="m-2 p-2 border border-gray-300"
              title="Phone Number"
              placeholder="(e.g. +6512345678)"
            />
            {formState.responded && (
              <input
                type="password"
                value={formState.passwordValue}
                onChange={handlePasswordChange}
                disabled={formState.passwordDisabled}
                className="m-2 p-2 border border-gray-300"
              />
            )}

            <button
              type="submit"
              className="m-2 p-2 bg-blue-500 text-white"
              disabled={formState.responded}
            >
              Submit
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
