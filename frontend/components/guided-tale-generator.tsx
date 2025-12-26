"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function GuidedTaleGenerator() {
    return (
        <div className="space-y-8">
            <Card>
                <CardHeader>
                    <CardTitle>Debug Mode</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-lg text-green-600 font-bold">
                        If you can see this, the page route and basic UI components work.
                    </p>
                    <p className="mt-4">
                        The crash is likely caused by one of the specific form components (Select, RadioGroup, etc.).
                    </p>
                </CardContent>
            </Card>
        </div>
    )
}
