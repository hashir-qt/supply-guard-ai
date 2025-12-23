export function DemoVideo() {
    return (
        <section className="py-12 px-6">
            <div className="container mx-auto">
                <div className="relative rounded-xl overflow-hidden border border-slate-200 shadow-2xl bg-slate-900 aspect-video max-w-5xl mx-auto ring-1 ring-slate-900/5">
                    {/* Placeholder for actual video */}
                    <div className="absolute inset-0 flex items-center justify-center bg-slate-950/50 z-10">
                        <div className="text-center space-y-4">
                            <div className="w-16 h-16 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-sm mx-auto cursor-pointer hover:bg-white/20 transition-all hover:scale-110">
                                <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M8 5v14l11-7z" />
                                </svg>
                            </div>
                            <p className="text-slate-300 text-sm font-medium tracking-wide uppercase">Watch Demo</p>
                        </div>
                    </div>

                    {/* Mock UI Background to look like a video frame if video is loading/paused */}
                    <div className="absolute inset-0 pointer-events-none opacity-40">
                        <div className="h-full w-full bg-gradient-to-br from-indigo-900/20 to-blue-900/20"></div>
                        {/* Abstract UI lines */}
                        <div className="absolute top-4 left-4 right-4 h-8 bg-white/5 rounded"></div>
                        <div className="absolute top-16 left-4 w-64 h-full bg-white/5 rounded"></div>
                        <div className="absolute top-16 right-4 left-72 h-full bg-white/5 rounded"></div>
                    </div>
                </div>

                {/* Decorative glow behind the video */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-blue-500/10 blur-3xl -z-10 rounded-full opacity-50 pointer-events-none"></div>
            </div>
        </section>
    )
}
