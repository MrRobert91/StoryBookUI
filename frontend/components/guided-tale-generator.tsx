"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Loader2, Sparkles } from "lucide-react"

export default function GuidedTaleGenerator() {
    const [formData, setFormData] = useState({
        age: "",
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
                        Step 3: RadioGroup Check
                    </CardTitle>
                    <CardDescription>Now checking RadioGroup components.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Age Selection - RadioGroup */}
                    <div className="space-y-2">
                        <Label>Age Group (RadioGroup Test)</Label>
                        <RadioGroup
                            className="flex gap-4"
                            value={formData.age}
                            onValueChange={(val) => handleInputChange("age", val)}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="3-5" id="age-3-5" />
                                <Label htmlFor="age-3-5">3-5 Years</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="5-8" id="age-5-8" />
                                <Label htmlFor="age-5-8">6-8 Years</Label>
                            </div>
                        </RadioGroup>
                    </div>

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
