import { useState } from "react";
import { Inter } from "next/font/google";

interface FormState {
  responded: boolean;
  inputValue: string;
  usernameValue: string;
  whitelistedContacts: string[];
  newWhitelistedContact: string;
  passwordValue: string;
  passwordDisabled: boolean;
}

const inter = Inter({ subsets: ["latin"] });

function getInstructionalText(responded: boolean): string {
  return !responded
    ? "Step 1: Fill in your phone number (with country code)"
    : "Step 2: Fill in your OTP";
}

export default function Start() {
  const [formState, setFormState] = useState<FormState>({
    responded: false,
    inputValue: "",
    usernameValue: "",
    whitelistedContacts: [],
    newWhitelistedContact: "",
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

  const handleAddWhitelistedContact = () => {
    setFormState(prevFormState => ({
      ...prevFormState,
      whitelistedContacts: [
        ...prevFormState.whitelistedContacts,
        prevFormState.newWhitelistedContact,
      ],
      newWhitelistedContact: "",
    }));
  };

  const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setFormState({
      ...formState,
      passwordValue: event.target.value,
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

  return (
    <main
      className={`flex h-screen w-screen flex-col items-center justify-center p-24 ${inter.className}`}
    >
      <div className="mb-32 grid text-center w-1/2 h-1/2 relative">
        <div className="w-full h-full group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
          <h2 className={`mb-3 text-2xl font-semibold`}>
            {getInstructionalText(formState.responded)}
          </h2>

          <form
            onKeyDown={e => {
              if (e.key == "Enter") {
                e.preventDefault();
              }
            }}
            onSubmit={e => {
              e.preventDefault();
              handleSubmitFirstStep();
            }}
            className="flex flex-col gap-4 w-full"
          >
            <div className="flex flex-col items-start">
              <label
                htmlFor="phoneNumber"
                className="mb-1 text-base font-semibold"
              >
                Phone Number (no spaces)
              </label>
              <input
                type="text"
                id="phoneNumber"
                value={formState.inputValue}
                onChange={handleInputChange("inputValue")}
                disabled={formState.responded}
                className="p-2 border border-gray-300 w-full"
                title="Phone Number"
                placeholder="(e.g. 6512345678)"
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
                placeholder="(e.g. @abcde)"
              />
            </div>

            <div className="flex flex-col items-start">
              <label
                htmlFor="whitelistedContacts"
                className="mb-1 text-base font-semibold"
              >
                Whitelisted Contacts
              </label>
              <div className="flex gap-2 items-center flex-wrap w-full">
                {formState.whitelistedContacts.map((contact, index) => (
                  <div
                    key={index}
                    className="bg-gray-200 rounded p-2 flex items-center gap-2"
                  >
                    {contact}
                    <button
                      type="button"
                      onClick={() => {
                        const updatedContacts = [
                          ...formState.whitelistedContacts,
                        ];
                        updatedContacts.splice(index, 1);
                        setFormState({
                          ...formState,
                          whitelistedContacts: updatedContacts,
                        });
                      }}
                      className="text-red-500"
                    >
                      X
                    </button>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex flex-col items-start">
              <div className="flex items-center gap-2 flex-wrap w-full">
                <div className="flex-grow">
                  <input
                    type="text"
                    id="whitelistedContacts"
                    value={formState.newWhitelistedContact}
                    onChange={handleInputChange("newWhitelistedContact")}
                    disabled={formState.responded}
                    className="p-2 border border-gray-300 w-full rounded-lg"
                    title="Whitelisted Contacts"
                    placeholder="Enter whitelisted contacts"
                  />
                </div>
                <button
                  type="button"
                  onClick={handleAddWhitelistedContact}
                  disabled={formState.responded}
                  className="p-2 bg-blue-500 text-white rounded-lg"
                >
                  Add
                </button>
              </div>
            </div>

            {formState.responded && (
              <div className="flex flex-col items-start col-span-2">
                <label
                  htmlFor="password"
                  className="mb-1 text-base font-semibold"
                >
                  OTP
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
            <button
              type="submit"
              // onClick={handleSubmitFirstStep}
              className={`col-span-2 flex items-center justify-center m-2 p-2 bg-blue-500 text-white relative w-full h-[45px] rounded-lg`}
              disabled={formState.responded}
            >
              Submit
              {loading && (
                <div className="object-contain grid place-items-center rounded-lg p-6">
                  <svg
                    className="text-gray-300 animate-spin"
                    viewBox="0 0 64 64"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                  >
                    {/* ... (spinner path data) */}
                    <path
                      d="M32 3C35.8083 3 39.5794 3.75011 43.0978 5.20749C46.6163 6.66488 49.8132 8.80101 52.5061 11.4939C55.199 14.1868 57.3351 17.3837 58.7925 20.9022C60.2499 24.4206 61 28.1917 61 32C61 35.8083 60.2499 39.5794 58.7925 43.0978C57.3351 46.6163 55.199 49.8132 52.5061 52.5061C49.8132 55.199 46.6163 57.3351 43.0978 58.7925C39.5794 60.2499 35.8083 61 32 61C28.1917 61 24.4206 60.2499 20.9022 58.7925C17.3837 57.3351 14.1868 55.199 11.4939 52.5061C8.801 49.8132 6.66487 46.6163 5.20749 43.0978C3.7501 39.5794 3 35.8083 3 32C3 28.1917 3.75011 24.4206 5.2075 20.9022C6.66489 17.3837 8.80101 14.1868 11.4939 11.4939C14.1868 8.80099 17.3838 6.66487 20.9022 5.20749C24.4206 3.7501 28.1917 3 32 3L32 3Z"
                      stroke="currentColor"
                      stroke-width="5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    ></path>
                    <path
                      d="M32 3C36.5778 3 41.0906 4.08374 45.1692 6.16256C49.2477 8.24138 52.7762 11.2562 55.466 14.9605C58.1558 18.6647 59.9304 22.9531 60.6448 27.4748C61.3591 31.9965 60.9928 36.6232 59.5759 40.9762"
                      stroke="currentColor"
                      stroke-width="5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      className="text-gray-900"
                    ></path>
                  </svg>
                </div>
              )}
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
