"use client"
import { X } from "lucide-react"

interface StripeModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function StripeModal({ isOpen, onClose }: StripeModalProps) {
  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      onClick={onClose} // Cierra el modal al hacer clic fuera
    >
      <div
        className="bg-white rounded-lg max-w-md w-full p-6 shadow-lg relative"
        onClick={(e) => e.stopPropagation()} // Evita que el clic dentro del modal lo cierre
      >
        <button onClick={onClose} className="absolute top-4 right-4 p-2 hover:bg-gray-100 rounded-full">
          <X className="h-5 w-5 text-gray-500" />
        </button>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Actualizar a Plan Plus</h2>
        <p className="text-gray-700 mb-6">
          ¡Gracias por tu interés! La integración con Stripe para la gestión de suscripciones está{" "}
          <span className="font-semibold text-purple-600">próximamente disponible</span>.
        </p>
        <p className="text-gray-600 text-sm">
          Mientras tanto, puedes seguir disfrutando de tus cuentos. ¡Te avisaremos cuando esta función esté lista!
        </p>
        <div className="mt-6 text-right">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 transition-colors"
          >
            Entendido
          </button>
        </div>
      </div>
    </div>
  )
}
