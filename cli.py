import json

from core.reddit_api import RedditAPI
from core.gemini_api import GeminiAPI
from models.idea import Idea
from database.database import IdeaDatabase
from utils.logger import logger
from config.config import Config


def main():
    Config()
    reddit_api = RedditAPI()
    gemini_api = GeminiAPI()
    idea_db = IdeaDatabase()

    if not reddit_api.reddit:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Reddit")
        return

    if not gemini_api.model:
        logger.error("Não foi possível iniciar a aplicação pois não foi estabelecida a conexão com a API do Gemini")
        return

    # Obtém posts e comentários do Reddit
    # posts_data = reddit_api.get_posts_and_comments()

    posts_data = [
      {
        "comments": [
          {
            "author": "Chelsea_M_Williams",
            "created": "2025-01-02 12:15:48",
            "text": "I have a bunch of free resources for finances for businesses (ie. Financial Success Guides, Info on how to choose an entity type, CFO checklist, KPIs, etc.) - [https://www.moneymastery.work/free-tools-access](https://www.moneymastery.work/free-tools-access) I started a new podcast, Always and Never About Money, for both personal and business finances. It\"s free to listen to all episodes - [https://itsalwaysandneveraboutmoney.buzzsprout.com/share](https://itsalwaysandneveraboutmoney.buzzsprout.com/share)",
            "upvotes": 4
          },
          {
            "author": "John_Gouldson",
            "created": "2025-01-02 11:04:16",
            "text": "Love this idea. Here you go, a free link to one of our yachting and lifestyle magazines. Ton of cool stuff for cars, planes and such. Pretty fun read. Enjoy! : [https://iyblue.com/magazine/iybluemag007.pdf](https://iyblue.com/magazine/iybluemag007.pdf)",
            "upvotes": 2
          },
          {
            "author": "Suly18",
            "created": "2025-01-02 12:01:11",
            "text": "this is great! i run a digital marketing company helping businesses get leads/sales & i’d love to offer a 33% discount off our services if anyone is interested",
            "upvotes": 2
          },
          {
            "author": "hanslee201",
            "created": "2025-01-02 15:44:47",
            "text": "Hi! My name is Hans and I lead the partnership efforts at [**Unblocked Brands**](http://unblockedbrands.com). We recently launched a product called **Passport**. It’s a **push notification tool** that helps you cut through the noise of the social media algorithm, so when you announce new products or videos/content, instead of hoping people will see it via IG (2% avg engagement rate)or an email newsletter (15-20% avg open rate), it would be sent to people’s phones as a push notification (**90% avg engagement rate**), so they definitely see it (100% delivery). **^(TD&LR)** Here’s what makes push notifications a game-changer: 🔹 **Immediate attention**: 40% of push notifications are viewed within an hour (vs 7.5 hours for email). 🔹 **No gatekeepers**: You decide when and how to engage your audience. 🔹 **Your brand, your rules**: Deliver exclusive updates, perks, or offers right to their device. As my first post here on r/Entrepreneur, I\"d be happy to provide a **free Growth Plan** ($399/mo) to anyone that signs up **by Jan 9th**! 🔥 Free Sign-Up [**here**](http://unblk.co/tythursday). 💪 Also receive free support by joining our Slack Channel [**here**](https://join.slack.com/t/unblockedbrands/shared_invite/zt-2vj8itpmu-gjV7X1lzIpWcB3qd1cPG~w).",
            "upvotes": 2
          },
          {
            "author": "heythisischris",
            "created": "2025-01-02 19:23:09",
            "text": "Hey ya\"ll! Offering a free week Tabchat AI. Tabchat AI is a Chrome extension that lets you chat directly with your active tabs. We securely scrape the HTML data from your DOM, send it over to our LLM, and viola- you\"re able to receive AI assistance with any website you\"re currently browsing. The possibilities, as you might imagine, are endless. Need help with a forum post? Done. Seeing if a product is worth purchasing? We can help. Need to extract data from a table? Piece of cake. In short: • Chat with any tab you have open • Easily extract unstructured data to CSV/JSON • Summarize articles & grab key points • Pick up on hidden context you might not see at first • Enormous 300k context powered by Amazon Nova Only $9.99/month for unlimited usage- get started with a 7 day free trial! Let me know what you think. Open to any and all feedback. Chrome Extension URL: https://chromewebstore.google.com/detail/tabchat-ai/belpggoeapomplfgocfednggkbimicph",
            "upvotes": 2
          },
          {
            "author": "Feisty_Attorney_3811",
            "created": "2025-01-02 23:32:20",
            "text": "Anyone looking to get into investing in stocks? I have a referral code for Questrade that I can provide for up to 10 people. If you use the code it will start you off with $50! Happy to send it to whoever could use the promotion.",
            "upvotes": 1
          },
          {
            "author": "Virtual_Welder_2467",
            "created": "2025-01-03 10:10:49",
            "text": "Want to receive some insights about your project or website? I\"m here to help you! I\"m a software developer with a lot of experience on the web field and i\"m sure that i can give some advices about your online presence, send me a DM and i will be checking your website, if i find something that can be improved, i will be telling you!",
            "upvotes": 1
          },
          {
            "author": "Hopeful_Piglet2416",
            "created": "2025-01-03 16:21:09",
            "text": "Happy New Year everyone! anyone who has a brilliant business idea that\"s not capital intensive for this year 2025?",
            "upvotes": 1
          },
          {
            "author": "johnrich85",
            "created": "2025-01-03 16:43:55",
            "text": "Hey all. Im currently offering lifetime membership to Listable (no code directory builder) for a one off fee. Check it out if interested: https://get-listable.com",
            "upvotes": 1
          }
        ],
        "id": "1hrqg5q",
        "num_comments": 10,
        "text": "**Your opportunity to thank the** /r/Entrepreneur **community by offering free stuff, contests, discounts, electronic courses, ebooks and the best deals you know of.** Please consolidate such offers here! Since this thread can fill up quickly, consider sorting the comments by \"new\" (instead of \"best\" or \"top\") to see the newest posts.",
        "title": "Thank you Thursday! - January 02, 2025",
        "upvotes": 4,
        "url": "https://www.reddit.com/r/Entrepreneur/comments/1hrqg5q/thank_you_thursday_january_02_2025/"
      }
    ]

    for post in posts_data:
        full_text = f"Post: {post['title']}\n{post['text']}\n"
        logger.info(f"Analisando o post: {post['title']} ({post['id']})")
        logger.info(f"Upvotes: {post['upvotes']}, Número de comentários: {post['num_comments']}")
        for comment in post['comments']:
            full_text += f"Comment: {comment['text']}\n"
            logger.info(f"  - {comment['author']}: {comment['text'][:50]}... (Upvotes: {comment['upvotes']})")

        # Analisa o texto usando a API do Gemini
        # analysis_result = gemini_api.analyze_with_gemini(full_text)

        analysis_result = {
            "post_analysis": {
                "insights": [
                    {
                        "problem": "Businesses struggle to effectively reach their audience with important updates and content, facing low engagement on social media and email.",
                        "saas_product": {
                            "description": "PushPro Engage is a SaaS platform that enables businesses to send push notifications directly to their audience\"s phones, ensuring immediate attention and high engagement rates. It bypasses the limitations of social media algorithms and the low open rates of email newsletters. The platform offers customizable notifications, user segmentation and detailed analytics, providing a comprehensive solution for audience engagement.",
                            "differentiators": [
                                "High engagement rates compared to email and social media",
                                "Guaranteed delivery",
                                "Ability to segment and target users effectively",
                                "Real-time analytics dashboard to track performance"
                            ],
                            "features": [
                                "Customizable push notifications",
                                "User segmentation",
                                "Real-time analytics",
                                "Scheduled notifications",
                                "Integration with other marketing tools"
                            ],
                            "implementation_score": 3,
                            "market_viability_score": 75,
                            "name": "PushPro Engage"
                        },
                        "solution": "A push notification tool designed to bypass algorithm limitations and guarantee delivery to users\" mobile phones."
                    },
                    {
                        "problem": "Users often need to extract information or interact with the content of websites they are currently browsing, lacking a seamless way to do so.",
                        "saas_product": {
                            "description": "TabWise AI is a browser extension that lets users interact directly with any open web page using AI. It allows users to summarize, extract data, and engage in contextual conversations with the current webpage, simplifying workflows and boosting productivity.  The extension uses a large language model for advanced features, ensuring accurate and efficient results.",
                            "differentiators": [
                                "Direct interaction with live webpages, not just pre-set knowledge",
                                "Ability to extract and export data from tables and unstructured content",
                                "Context awareness for better assistance and summaries",
                                "Integration with a cutting-edge large language model (LLM)"
                            ],
                            "features": [
                                "Chat with any tab",
                                "Data extraction (CSV/JSON)",
                                "Article summarization",
                                "Context-aware assistance",
                                "Integration with a large language model (LLM)"
                            ],
                            "implementation_score": 4,
                            "market_viability_score": 80,
                            "name": "TabWise AI"
                        },
                        "solution": "A browser extension that allows users to directly interact with the content of their active tabs using AI."
                    },
                    {
                        "problem": "Business owners are seeking new business opportunities that are not capital intensive.",
                        "saas_product": {
                            "description": "IdeaSpark is a SaaS platform for generating, validating, and refining business ideas that require low initial capital. The platform uses user-input data, market trends and AI to generate and validate ideas. It helps users discover opportunities in specific industries or niches, assess their feasibility and create basic business models. It aims to be a catalyst for entrepreneurial thinking by providing a structured approach to idea generation and validation.",
                            "differentiators": [
                                "Focus on low-capital business models",
                                "User-driven insights and community feedback",
                                "Integration with market analysis tools for real-time data",
                                "AI-powered idea validation that goes beyond superficial analysis"
                            ],
                            "features": [
                                "AI-powered idea generation",
                                "Market validation tools",
                                "Low-capital business model templates",
                                "User-driven feedback system",
                                "Opportunity assessment reports"
                            ],
                            "implementation_score": 2,
                            "market_viability_score": 60,
                            "name": "IdeaSpark"
                        },
                        "solution": "A platform that generates and validates business ideas through user input, market analysis and AI insights."
                    },
                    {
                        "problem": "Businesses and entrepreneurs need an easy way to build online directories without coding",
                        "saas_product": {
                            "description": "DirectoryEase is a no-code SaaS platform designed to enable anyone to create their online directory without needing to write a single line of code. It offers a wide variety of customizable templates, intuitive drag-and-drop editors and a suite of features to manage listings, users, and content. It\"s ideal for small businesses, community groups, and entrepreneurs who want to launch a directory quickly and affordably.",
                            "differentiators": [
                                "Intuitive no-code interface suitable for non-technical users",
                                "Highly customizable and feature-rich directory templates",
                                "Simplified user onboarding and directory management",
                                "Affordable pricing tiers for different needs",
                                "Integrations for monetization (payment gateways, advertisement)"
                            ],
                            "features": [
                                "Drag and drop directory builder",
                                "Customizable directory templates",
                                "User and listing management",
                                "Search and filter functionalities",
                                "Integration with payment gateways"
                            ],
                            "implementation_score": 3,
                            "market_viability_score": 85,
                            "name": "DirectoryEase"
                        },
                        "solution": "A no-code directory builder with a focus on ease of use and customization, offering a low entry barrier for creating online directories."
                    }
                ],
                "post_description": "Opportunity to thank the /r/Entrepreneur community by offering free stuff, contests, discounts, electronic courses, ebooks and the best deals you know of.",
                "post_title": "Thank you Thursday! - January 02, 2025"
            }
        }

        if analysis_result and analysis_result.get("post_analysis").get("insights"):
            analysis_result_list = analysis_result.get("post_analysis").get("insights")
            for result in analysis_result_list:
                idea = Idea(
                    reddit_content_id=post['id'],
                    product_name=result.get("saas_product").get('name'),
                    problem=result.get('problem'),
                    solution_description=result.get("saas_product").get('description'),
                    implementation_score=result.get("saas_product").get('implementation_score'),
                    market_viability_score=result.get("saas_product").get('market_viability_score'),
                    differentials=result.get("saas_product").get('differentiators'),
                    features=result.get("saas_product").get('features'),
                )
                if idea_db.add_idea(idea):
                    logger.info(f"Ideia adicionada: {idea}")
                    print(f"Ideia adicionada com sucesso: {idea.product_name}")
                else:
                    logger.warning(f"Não foi possível adicionar a ideia, pois ela já existe na base")
                    print(f"Ideia com ID {idea.reddit_content_id} já existe.")
        else:
            logger.warning(f"Não foi encontrada uma ideia para o post: {post['title']}")

    print("\nExtração e análise concluída!")

    for idea in idea_db.get_all_ideas():
        print(f"Ideia: {idea}")


if __name__ == "__main__":
    main()