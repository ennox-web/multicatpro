const useMockSession = (session) => ({
    data: session,
    status: session ? 'authenticated' : 'unauthenticated',
    update: async() => {}
});

export default useMockSession;
