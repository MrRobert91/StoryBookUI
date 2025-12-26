"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
// Unused imports related to potentially problematic components
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Loader2, Sparkles, AlertCircle } from "lucide-react"

export default function GuidedTaleGenerator() {
    const [formData, setFormData] = useState({
        protagonistName: "",
        protagonistDesc: "",
    })

    const handleInputChange = (field: string, value: string) => {
        setFormData((prev) => ({
            ...prev,
            [field]: value,
        }))
    }

    return (
        <div className="space-y-8">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        Step 2: Basic Inputs Check
                    </CardTitle>
                    <CardDescription>Verify if Inputs and Buttons render correctly.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Protagonist - Basic Inputs */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="protagonistName">Protagonist Name</Label>
                            <Input
                                id="protagonistName"
                                placeholder="e.g. Luna"
                                value={formData.protagonistName}
                                onChange={(e) => handleInputChange("protagonistName", e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="protagonistDesc">Protagonist Description</Label>
                            <Input
                                id="protagonistDesc"
                                placeholder="e.g. A brave little cat"
                                value={formData.protagonistDesc}
                                onChange={(e) => handleInputChange("protagonistDesc", e.target.value)}
                            />
                        </div>
                    </div>

                    {/* Submit Button */}
                    <Button
                        className="w-full bg-teal-600 hover:bg-teal-700 text-lg py-6"
                    >
                        <Sparkles className="mr-2 h-5 w-5" />
                        Test Button
                    </Button>
                </CardContent>
            </Card>
        </div>
    )
}
