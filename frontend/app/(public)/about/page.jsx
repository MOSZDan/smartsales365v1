import Link from 'next/link'
import PageTitle from '@/components/PageTitle'

export default function AboutPage() {
    return (
        <div className="mx-6">
            <div className="max-w-7xl mx-auto py-12">
                <PageTitle title="About Us" />

                <div className="mt-8 space-y-8">
                    <section className="bg-white rounded-lg shadow-sm p-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome to GoCart Plus</h2>
                        <p className="text-gray-600 leading-relaxed">
                            GoCart Plus is your ultimate destination for the latest and smartest gadgets.
                            From smartphones and smartwatches to essential accessories, we bring you the
                            best in innovation — all in one place.
                        </p>
                    </section>

                    <section className="bg-white rounded-lg shadow-sm p-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h2>
                        <p className="text-gray-600 leading-relaxed">
                            We strive to provide a seamless shopping experience by connecting customers
                            with trusted vendors and quality products. Our multi-vendor platform empowers
                            entrepreneurs to grow their businesses while ensuring customers receive the
                            best products at competitive prices.
                        </p>
                    </section>

                    <section className="bg-white rounded-lg shadow-sm p-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">What We Offer</h2>
                        <div className="grid md:grid-cols-2 gap-6 mt-4">
                            <div>
                                <h3 className="font-semibold text-gray-900 mb-2">For Customers</h3>
                                <ul className="list-disc list-inside text-gray-600 space-y-2">
                                    <li>Wide selection of products from multiple vendors</li>
                                    <li>Secure payment options including Stripe and COD</li>
                                    <li>Fast and reliable shipping</li>
                                    <li>Customer reviews and ratings</li>
                                    <li>24/7 customer support</li>
                                </ul>
                            </div>
                            <div>
                                <h3 className="font-semibold text-gray-900 mb-2">For Vendors</h3>
                                <ul className="list-disc list-inside text-gray-600 space-y-2">
                                    <li>Easy store setup and management</li>
                                    <li>Comprehensive dashboard with analytics</li>
                                    <li>Order management system</li>
                                    <li>Marketing and promotional tools</li>
                                    <li>Plus membership benefits</li>
                                </ul>
                            </div>
                        </div>
                    </section>

                    <section className="bg-white rounded-lg shadow-sm p-8">
                        <h2 className="text-2xl font-bold text-gray-900 mb-4">Why Choose Us?</h2>
                        <div className="grid md:grid-cols-3 gap-6 mt-4">
                            <div className="text-center">
                                <div className="text-4xl mb-2">🚀</div>
                                <h3 className="font-semibold text-gray-900 mb-2">Fast Delivery</h3>
                                <p className="text-gray-600 text-sm">Quick and reliable shipping to your doorstep</p>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl mb-2">🔒</div>
                                <h3 className="font-semibold text-gray-900 mb-2">Secure Payments</h3>
                                <p className="text-gray-600 text-sm">Multiple secure payment options available</p>
                            </div>
                            <div className="text-center">
                                <div className="text-4xl mb-2">⭐</div>
                                <h3 className="font-semibold text-gray-900 mb-2">Quality Products</h3>
                                <p className="text-gray-600 text-sm">Only the best products from trusted vendors</p>
                            </div>
                        </div>
                    </section>

                    <section className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-sm p-8 text-white text-center">
                        <h2 className="text-2xl font-bold mb-4">Ready to Get Started?</h2>
                        <p className="mb-6">Join thousands of satisfied customers and vendors on our platform</p>
                        <div className="flex justify-center gap-4">
                            <Link
                                href="/shop"
                                className="bg-white text-indigo-600 px-6 py-2 rounded-full font-medium hover:bg-gray-100 transition"
                            >
                                Start Shopping
                            </Link>
                            <Link
                                href="/create-store"
                                className="bg-transparent border-2 border-white text-white px-6 py-2 rounded-full font-medium hover:bg-white hover:text-indigo-600 transition"
                            >
                                Create a Store
                            </Link>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    )
}