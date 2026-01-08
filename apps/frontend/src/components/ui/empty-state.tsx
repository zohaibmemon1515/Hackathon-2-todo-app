import { ExclamationTriangleIcon, InformationCircleIcon } from '@heroicons/react/24/outline';

interface EmptyStateProps {
  title: string;
  message: string;
  icon?: 'info' | 'warning' | 'error';
  action?: {
    text: string;
    onClick: () => void;
  };
}

export default function EmptyState({ title, message, icon = 'info', action }: EmptyStateProps) {
  const getIcon = () => {
    switch (icon) {
      case 'warning':
        return <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-yellow-400" />;
      case 'error':
        return <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-red-400" />;
      case 'info':
      default:
        return <InformationCircleIcon className="mx-auto h-12 w-12 text-gray-400" />;
    }
  };

  return (
    <div className="text-center py-12">
      {getIcon()}
      <h3 className="mt-2 text-sm font-medium text-gray-900">{title}</h3>
      <p className="mt-1 text-sm text-gray-500">{message}</p>
      {action && (
        <div className="mt-6">
          <button
            type="button"
            onClick={action.onClick}
            className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {action.text}
          </button>
        </div>
      )}
    </div>
  );
}