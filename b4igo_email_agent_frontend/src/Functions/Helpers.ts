import React from "react";

// TODO: back off if no changes maybe or no user interaction?0
export const useRepeatingFetch = <T>(
    fetchFn: () => Promise<T>,
    setFn: (data: T) => void,
    intervalMs: number
) => {
    React.useEffect(() => {
        const fetch = () => {
            fetchFn()
                .then(setFn)
                .catch(console.error);
        };

        fetch();

        const interval = setInterval(fetch, intervalMs);

        return () => clearInterval(interval);
    }, [fetchFn, setFn, intervalMs]);
};
