def generate_dashboard_insights(business, campaigns, referrals):

    insights = []

    pending = referrals.filter(status="pending").count()

    if pending:
        insights.append({
            "icon": "fa-solid fa-hourglass-half",
            "color": "warning",
            "title": "Pending Referrals",
            "message": f"You have {pending} referral(s) waiting for approval."
        })

    rewarded = referrals.filter(status="rewarded").count()

    if rewarded:
        insights.append({
            "icon": "fa-solid fa-gift",
            "color": "success",
            "title": "Rewards Issued",
            "message": f"You've rewarded {rewarded} referral(s)."
        })

    for campaign in campaigns:

        progress = campaign.progress_percentage

        if progress == 100:

            insights.append({

                "icon": "fa-solid fa-trophy",

                "color": "primary",

                "title": "Campaign Goal Reached",

                "message": f'"{campaign.title}" reached its referral goal.'

            })

        elif progress >= 80:

            insights.append({

                "icon": "fa-solid fa-chart-line",

                "color": "success",

                "title": "Campaign Almost Complete",

                "message": f'"{campaign.title}" is {progress}% complete.'

            })

    return insights[:3]