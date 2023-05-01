export const showToast = (toasts: any, toastType: string, title: string, description: string, placement: string="bottom-right", theme: string="dark") => {
    const toast = toasts.add({
      title: title,
      description: description,
      duration: 10000, // 0 or negative to avoid auto-remove
      placement: placement,
      type: toastType,  // success, info, error, warning
      theme: theme, // dark, light
      onClick: () => {},
      onRemove: () => {},
      // component: BootstrapToast, // allows to override toast component/template per toast
    });

    // toast.remove()
};