"use client";

import { AuthForm } from "@/components/auth-form";
import { SubmitButton } from "@/components/submit-button";
import { toast } from "@/components/toast";
import { useSession } from "next-auth/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useActionState, useEffect, useState } from "react";
import { type RegisterActionState, register } from "../actions";

export default function Page() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [isSuccessful, setIsSuccessful] = useState(false);

  const [state, formAction] = useActionState<RegisterActionState, FormData>(
    register,
    {
      status: "idle",
    }
  );

  const { update: updateSession } = useSession();

  useEffect(() => {
    if (state.status === "user_exists") {
      toast({ type: "error", description: "¡La cuenta ya existe!" });
    } else if (state.status === "failed") {
      toast({ type: "error", description: "¡Error al crear la cuenta!" });
    } else if (state.status === "invalid_data") {
      toast({
        type: "error",
        description: "¡Error al validar tu envío!",
      });
    } else if (state.status === "success") {
      toast({ type: "success", description: "¡Cuenta creada exitosamente!" });

      setIsSuccessful(true);
      updateSession();
      router.refresh();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.status]);

  const handleSubmit = (formData: FormData) => {
    setEmail(formData.get("email") as string);
    formAction(formData);
  };

  return (
    <div className="flex h-dvh w-screen items-start justify-center bg-background pt-12 md:items-center md:pt-0">
      <div className="flex w-full max-w-md flex-col gap-12 overflow-hidden rounded-2xl">
        <div className="flex flex-col items-center justify-center gap-2 px-4 text-center sm:px-16">
          <h3 className="font-semibold text-xl dark:text-zinc-50">Registrarse</h3>
          <p className="text-gray-500 text-sm dark:text-zinc-400">
            Crea una cuenta con tu correo y contraseña
          </p>
        </div>
        <AuthForm action={handleSubmit} defaultEmail={email}>
          <SubmitButton isSuccessful={isSuccessful}>Registrarse</SubmitButton>
          <p className="mt-4 text-center text-gray-600 text-sm dark:text-zinc-400">
            {"¿Ya tienes una cuenta? "}
            <Link
              className="font-semibold text-gray-800 hover:underline dark:text-zinc-200"
              href="/login"
            >
              Inicia sesión
            </Link>
            {" aquí."}
          </p>
        </AuthForm>
      </div>
    </div>
  );
}
