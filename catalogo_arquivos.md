## .DS_Store
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xb8 in position 295: invalid start byte
```

## postcss.config.mjs
```
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
  },
};

export default config;

```

## Dockerfile
```
# syntax=docker.io/docker/dockerfile:1

FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json* ./
RUN npm install

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Debug: Mostrar conteúdo dos arquivos de configuração
RUN echo "Conteúdo do next.config.ts:" && cat next.config.ts
RUN echo "Conteúdo do package.json:" && cat package.json

# Build the application
RUN npm run build

# Debug: Listar conteúdo do .next
RUN echo "Conteúdo da pasta .next:" && ls -la .next
RUN echo "Conteúdo da pasta .next/standalone:" && ls -la .next/standalone || echo "Pasta standalone não encontrada"

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Tentar copiar standalone ou todo o .next
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

## next-env.d.ts
```typescript
/// <reference types="next" />
/// <reference types="next/image-types/global" />

// NOTE: This file should not be edited
// see https://nextjs.org/docs/app/api-reference/config/typescript for more information.

```

## tailwind.config.ts
```typescript
import type { Config } from "tailwindcss";

export default {
    darkMode: ["class"],
    content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
  	extend: {
		backgroundImage: {
            'curve-1': 'url("/curve-1.png.webp")',
       },
  		colors: {
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			primary: {
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))'
  			},
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			chart: {
  				'1': 'hsl(var(--chart-1))',
  				'2': 'hsl(var(--chart-2))',
  				'3': 'hsl(var(--chart-3))',
  				'4': 'hsl(var(--chart-4))',
  				'5': 'hsl(var(--chart-5))'
  			}
  		},
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		keyframes: {
  			'accordion-down': {
  				from: {
  					height: '0'
  				},
  				to: {
  					height: 'var(--radix-accordion-content-height)'
  				}
  			},
  			'accordion-up': {
  				from: {
  					height: 'var(--radix-accordion-content-height)'
  				},
  				to: {
  					height: '0'
  				}
  			}
  		},
  		animation: {
  			'accordion-down': 'accordion-down 0.2s ease-out',
  			'accordion-up': 'accordion-up 0.2s ease-out'
  		}
  	}
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;

```

## .dockerignore
```
node_modules
.git
.next/cache
npm-debug.log
Dockerfile
.dockerignore
```

## components.json
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/app/[locale]/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

## tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}

```

## eslint.config.mjs
```
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;

```

## next.config.ts
```typescript
import createNextIntlPlugin from 'next-intl/plugin';
import type { NextConfig } from 'next';
 
const withNextIntl = createNextIntlPlugin();
 
const nextConfig: NextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  output: 'standalone',
};
 
export default withNextIntl(nextConfig);
```

## messages/en copy.json
```json
{
    "HomePage": {
      "title": "NextJS i18n Tutorial",
      "description": "Tutorial of how to manipulate i18n based on route path or domain with  Nextjs v15",
      "pricing": "Pricing",
      "docs": "Docs",
      "wall-of-love": "Wall of Love",
      "faq": "Faq"
    },
    "ContactPage": {
      "title": "Contact Page"
    },
    "HeroComponent": {
      "hero_title_part1": "Transform Real Problems",
       "hero_title_part2": "into",
      "hero_title_part3": "Successful Micro SaaS!",
      "hero_subtitle_part1": "Stop wasting time and money on business ideas no one wants.",
      "hero_subtitle_part2": "Access thousands of business ideas based on real problems.",
      "hero_discount": "$10 off for the first 50 users",
       "hero_remaining": "48 left",
        "hero_button": "Access IdeaForge DB",
         "hero_ideias_title_part1": "Access over 1000 ",
      "hero_ideias_title_part2": "successful ideas",
      "ideas": "en"
    },
    "IdeaCardComponent": {
      "differentials": "Differentials",
      "features": "Features",
      "implementation": "Implementation",
      "viability": "Viability"
    },
    "FeaturesComponent": {
      "all_in_one": "Complete and ready-to-use solution",
      "features_title_part1": "Boost Your Startup with",
      "features_title_part2": "Innovative Ideas!",
      "features_subtitle": "Launch Your SaaS with Speed: Let Us Handle Tedious Tasks, While You Build Your Brand.",
      "feature_title_1": "Database of Real-World Problems",
      "feature_description_1": "Browse a vast collection of business ideas based on genuine problems discussed by active online communities. Save time and focus on what really matters: building your brand.",
      "feature_title_2": "Database of Business Ideas",
      "feature_description_2": "Explore unexplored opportunities with AI-generated solutions, identifying market gaps and emerging trends. Find the perfect inspiration for your next micro SaaS.",
      "feature_title_3": "Weekly Updates",
      "feature_description_3": "Stay ahead of the competition with new ideas and trends added daily. Never miss a market opportunity with our continuous update system."
    },
    "PriceSection": {
      "title_part_1": "Don't waste time on boring things.",
      "title_part_2": "Get profitable really fast.",
      "card_tile_1": "Basic - Annual Access",
      "card_full_price": "$60.00",
      "card_discount_price": "$50,00",
      "card_description": "Pay once. Build unlimited products",
      "card_feature_1": "Weekly updates",
      "card_feature_2": "Unlimited consultations",
      "card_feature_3": "Idea Forge DB with +3000 ideas",
      "card_feature_4": "Advanced search with filters",
      "card_feature_5": "AI-driven feature suggestions",
      "call_to_action": "Access IdeaForge DB"
    },
    "faqSection": {
      "title": "Frequently Asked Questions",
      "sub-title": "Have another question? Contact me by email or send me a DM on twitter",
      "q1": "What does IdeaForge DB offer?",
      "r1": "IdeaForge DB offers access to a database of business ideas based on real problems discussed by real users on social media. With our subscription plan, you can access thousands of business ideas and save time and money. After purchase, you will have access to a control panel where you can filter ideas by niche, creation date, and popularity.",
      "q2": "Can I get a refund?",
      "r2": "No, IdeaForge DB is a non-refundable product. Please review the resources and benefits to ensure it meets your needs before making a purchase. If you have any questions, contact me by: ",
      "q3": "How often is IdeaForge DB updated?",
      "r3": "Our system updates the database daily. You will have access to new business ideas every day.",
      "q4": "What if I have problems or questions?",
      "r4": "If you encounter any problems or have questions, we are here to help you get the most out of IdeaForge DB. You can contact me by",
      "q5": "What type of content is in IdeaForge DB?",
      "r5": "IdeaForge DB contains a database with thousands of business ideas based on real problems discussed by real users on social media. You can filter ideas by niche, creation date, and popularity, all to help you understand and solve common user problems and validate your ideas.",
      "q6": "How do I access IdeaForge DB after purchase?",
      "r6": "After purchasing a subscription, you will receive an email with a link to access IdeaForge DB. Simply log in with your account details to explore the database."
    },
    "bottomSection": {
      "title": "Launch Your Startup to Market in Record Time!",
      "sub-title": "Save months on development and focus on what truly matters: growth and profit.",
      "call_to_action": "Access IdeaForge DB"
    },
    "FooterSection": {
      "text1": "Ignite Your Creativity.",
      "text2": "© 2024 IdeaForge. All rights reserved.",
      "text3": "IdeaForge Built by BeMySaaS"
    }
  }
```

## messages/pt copy.json
```json
{
  "HeaderComponent": {
    "call_to_action": "Inicie sua Jornada SaaS"
  },
  "HeroComponent": {
    "hero_title_part1": "Transforme problemas reais",
    "hero_title_part2": "em",
    "hero_title_part3": "micro SaaS de sucesso!",
    "hero_subtitle_part1": "Para empreendedores e visionários do SaaS: Aceite o desafio e construa seu caminho no mundo SaaS com ferramentas prontas, ideias validadas, e suporte especializado.",
    "hero_subtitle_part2": "",
    "hero_discount": "R$100 de desconto",
    "hero_remaining": "48 vagas restantes",
    "hero_ideias_title_part1": "Acesse mais de 3000 ideias",
    "hero_ideias_title_part2": "validadas e prontas para ação",
    "call_to_action": "Inicie sua Jornada SaaS",
    "ideas": "pt"
  },
  "ValuePropositionComponent": {
    "all_in_one": "Solução completa e validada",
    "features_title_part1": "Acelere sua startup",
    "features_subtitle": "Converta problemas reais em sucessos de micro SaaS através de ideias validadas, modelos prontos e consultoria especializada.",
    "feature_title_1": "Ideias validadas",
    "feature_description_1": "Exploração de um banco abrangente de milhares de ideias analisadas para rápida validação e adaptação ao mercado.",
    "feature_title_2": "Modelos de negócio com I.A",
    "feature_description_2": "Utilização de inteligência artificial para criar planos de negócios otimizados, economizando tempo e recursos.",
    "feature_title_3": "Consultoria personalizada",
    "feature_description_3": "Apoio sob medida em cada etapa do desenvolvimento, garantindo a eficácia e o sucesso do seu projeto SaaS.",
    "feature_title_4": "Ferramentas integradas",
    "feature_description_4": "Criação de páginas personalizáveis com integração rápida para marketing e lançamento."
  },
  "IdeaCardComponent": {
    "differentials": "Diferenciais",
    "features": "Funcionalidades",
    "implementation": "Implementação",
    "viability": "Viabilidade"
  },
  "FeaturesComponent": {
    "all_in_one": "Solução completa e validada",
    "features_title_part1": "Acelere sua startup com",
    "features_title_part2": "Ideias validadas!",
    "features_subtitle": "Economize tempo na pesquisa de mercado e comece a construir seu SaaS com as melhores ideias do mercado.",
    "feature_title_1": "Banco de dados de problemas reais",
    "feature_description_1": "Explore ideias de negócios baseadas em problemas genuínos discutidos por comunidades online ativas. Foque no que importa: construir um produto de sucesso.",
    "feature_title_2": "Banco de Dados de Ideias de Negócios",
    "feature_description_2": "Descubra oportunidades inexploradas com soluções geradas por IA, identificando lacunas de mercado e tendências emergentes. Encontre a ideia perfeita para seu próximo Micro SaaS.",
    "feature_title_3": "Atualizações constantes",
    "feature_description_3": "Receba novas ideias semanalmente e mantenha-se à frente da concorrência. Nosso banco de dados está sempre atualizado com as últimas tendências."
  },
  "PriceSection": {
    "title_part_1": "Pare de perder tempo pesquisando.",
    "title_part_2": "Acesse ideias validadas e construa rápido.",
    "card_tile_1": "Básico - Acesso Anual",
    "card_full_price": "R$360,00",
    "card_discount_price": "R$260,00",
    "card_description": "Pagamento único. Crie negócios ilimitados.",
    "card_feature_1": "Atualizações semanais",
    "card_feature_2": "Consultas ilimitadas",
    "card_feature_3": "IdeaForge DB com +3000 ideias",
    "card_feature_4": "Pesquisa avançada com filtros",
    "card_feature_5": "Sugestões de funcionalidades com IA",
    "call_to_action": "Inicie sua Jornada SaaS"
  },
  "faqSection": {
    "title": "Perguntas Frequentes",
    "sub-title": "Tem mais dúvidas? Entre em contato por e-mail ou WhatsApp",
    "q1": "O que o IdeaForge DB oferece?",
    "r1": "O IdeaForge DB oferece acesso a um banco de dados com milhares de ideias de negócios baseadas em problemas reais discutidos por usuários de redes sociais. Você poderá filtrar as ideias por nicho, data de criação e popularidade para encontrar oportunidades validadas e economizar tempo no desenvolvimento de sua startup.",
    "q2": "O IdeaForge DB já está disponível?",
    "r2": "Estamos finalizando os detalhes do IdeaForge! Cadastre-se agora para ser um dos primeiros a acessar no lançamento e aproveite descontos exclusivos.",
    "q3": "Posso obter um reembolso?",
    "r3": "O IdeaForge DB é um produto não reembolsável. Por favor, revise os recursos e benefícios antes de adquirir. Se tiver dúvidas, entre em contato conosco.",
    "q4": "Com que frequência o IdeaForge DB é atualizado?",
    "r4": "Nosso banco de dados é atualizado semanalmente com novas ideias e tendências. Você terá acesso constante a oportunidades frescas.",
    "q5": "Que tipo de conteúdo está no IdeaForge DB?",
    "r5": "Nosso banco de dados contém ideias de negócios baseadas em problemas reais discutidos por usuários em redes sociais. Além disso, oferecemos sugestões de funcionalidades geradas por IA para ajudar você a criar soluções completas.",
    "q6": "Como acesso o IdeaForge DB após a compra?",
    "r6": "Após a compra, você receberá um e-mail com os detalhes de acesso à plataforma. Faça login para explorar o banco de dados e começar a construir sua startup."
  },
  "bottomSection": {
    "title": "Receba Ideias Novas Toda Semana!",
    "sub-title": "Assine nossa newsletter e descubra semanalmente ideias inovadoras, insights de mercado e dicas exclusivas diretamente no seu e-mail.",
    "call_to_action": "Inicie sua Jornada SaaS"
  },
  "FooterSection": {
    "text1": "Desperte sua criatividade.",
    "text2": "© 2024 IdeaForge. Todos os direitos reservados.",
    "text3": "IdeaForge Construído por BeMySaaS"
  },
  "WaitlistBenefitsSection": {
    "title": "Por que se inscrever na lista de espera?",
    "b1": "Acesso antecipado ao nosso banco de dados de 3.000+ ideias de negócios.",
    "b2": "Um desconto especial quando lançarmos.",
    "b3": "Seja o primeiro a explorar ideias de negócios validadas e tendências.",
    "b4": "Receba atualizações sobre o desenvolvimento do produto e suas características.",
    "call_to_action": "Inicie sua Jornada SaaS"
  },
  "EmailCaptureForm": {
    "title": "Junte-se à lista de espera",
    "alert": "Nome e Email são obrigatórios.",
    "name": "Nome",
    "email": "Email",
    "phone": "Celular (Opcional)",
    "btn": "Enviar",
    "msg": "Enviado com sucesso"
  },
  "HowItWorks": {
    "title": "Transforme Sua Ideia em Realidade",
    "sub-title": "A Jornada Completa para Lançar Seu Produto SaaS com Sucesso",
    "feature_title_1": "Explore um Mundo de Ideias",
    "feature_description_1": "Mergulhe em nosso extenso banco de dados com milhares de ideias de negócios inspiradas em desafios reais do mercado. Encontre a inspiração perfeita para iniciar seu projeto.",
    "feature_title_2": "Planeje com Inteligência Artificial",
    "feature_description_2": "Utilize nosso poderoso Agente de I.A. para desenvolver planos de negócios otimizados com o modelo Canvas ou Lean. Economize tempo e recursos com insights estratégicos automatizados.",
    "feature_title_3": "Crie Sua Presença Online",
    "feature_description_3": "Construa sua landing page com nossas ferramentas e templates intuitivos. Lance campanhas de marketing rapidamente com páginas personalizáveis e integração facilitada.",
    "feature_title_4": "Apoio Especializado Sempre que Precisar ",
    "feature_description_4": "Conte com nosso time de especialistas para orientação em qualquer etapa do processo. Receba suporte sob medida para maximizar o potencial do seu projeto SaaS.",
    "feature_title_5": "Lançamento de Sucesso",
    "feature_description_5": "Dê vida à sua ideia e veja seu produto conquistar o mercado. Com nossa plataforma, você estará no caminho certo para alcançar o sucesso."
  },
  "TestimonialsSection": {
    "title": "O que nossos clientes dizem",
      "name_1": "Ana Silva",
      "role_1": "Empreendedora",
      "text_1": "O IdeaForge DB foi uma verdadeira revolução para o meu negócio. Encontrei a ideia perfeita para minha startup e economizei meses de pesquisa. Recomendo a todos os empreendedores!",
      "name_2": "Pedro Santos",
      "role_2": "Empreendedor Digital",
      "text_2": "A plataforma IdeaForge é incrível! Encontrei uma ideia de negócio que me apaixonei e pude começar a trabalhar imediatamente. O suporte da equipe foi excepcional. Obrigado!",
      "name_3": "Mario Oliveira",
      "role_3": "Desenvolvedor de Software",
      "text_3": "O IdeaForge DB é uma ferramenta essencial para qualquer pessoa que deseja iniciar um negócio SaaS. As ideias são inovadoras e fáceis de implementar. Estou muito satisfeita com os resultados!"
  }
}
```

## messages/pt.json
```json
{
  "HeaderComponent": {
    "call_to_action": "Comece Sua Jornada SaaS Agora"
  },
  "HeroComponent": {
    "hero_title_part1": "Transforme problemas reais",
    "hero_title_part2": "em",
    "hero_title_part3": "Micro SaaS de Sucesso!",
    "hero_subtitle_part1": "Para empreendedores e visionários do SaaS: Encare o desafio e construa seu caminho com ferramentas prontas, ideias validadas e suporte especializado.",
    "hero_subtitle_part2": "",
    "hero_discount": "Economize R$100",
    "hero_remaining": "Apenas 48 vagas disponíveis",
    "hero_ideias_title_part1": "Acesse Mais de 3.000 Ideias",
    "hero_ideias_title_part2": "Validadas e Prontas para Ação",
    "call_to_action": "Inicie Sua Jornada SaaS",
    "ideas": "pt"
  },
  "ValuePropositionComponent": {
    "all_in_one": "A Solução Completa e Validada para Seu Negócio",
    "features_title_part1": "Impulsione Sua Startup",
    "features_subtitle": "Transforme problemas reais em sucessos de micro SaaS com ideias validadas, modelos prontos e consultoria especializada.",
    "feature_title_1": "Ideias Validadas",
    "feature_description_1": "Explore um banco abrangente de ideias analisadas para rápida validação e adaptação ao mercado.",
    "feature_title_2": "Modelos de Negócio com I.A",
    "feature_description_2": "Crie planos de negócios otimizados com IA, economizando tempo e recursos.",
    "feature_title_3": "Consultoria Personalizada",
    "feature_description_3": "Receba apoio personalizado em cada etapa do desenvolvimento, garantindo o sucesso do seu projeto.",
    "feature_title_4": "Ferramentas Integradas",
    "feature_description_4": "Desenvolva páginas personalizáveis com integração rápida para marketing e lançamento."
  },
  "IdeaCardComponent": {
    "differentials": "Diferenciais Únicos",
    "features": "Principais Funcionalidades",
    "implementation": "Facilidade de Implementação",
    "viability": "Alta Viabilidade de Mercado"
  },
  "FeaturesComponent": {
    "all_in_one": "A Solução Completa e Validada para Seu Negócio",
    "features_title_part1": "Impulsione Sua Startup com",
    "features_title_part2": "Ideias Validadas!",
    "features_subtitle": "Economize tempo e comece a construir seu SaaS com as melhores ideias do mercado.",
    "feature_title_1": "Banco de Dados de Problemas Reais",
    "feature_description_1": "Explore ideias de negócios baseadas em problemas genuínos discutidos por comunidades online. Concentre-se no essencial: construir um produto de sucesso.",
    "feature_title_2": "Banco de Dados de Ideias de Negócios",
    "feature_description_2": "Descubra oportunidades inexploradas com soluções geradas por IA, identificando lacunas de mercado e tendências emergentes.",
    "feature_title_3": "Atualizações Constantes",
    "feature_description_3": "Receba novas ideias semanalmente para se manter à frente da concorrência."
  },
  "PriceSection": {
    "title_part_1": "Pare de Procurar.",
    "title_part_2": "Comece a Construir.",
    "card_tile_1": "Básico - Acesso Anual",
    "card_full_price": "R$360,00",
    "card_discount_price": "R$260,00",
    "card_description": "Pagamento único. Crie negócios ilimitados com planos acessíveis.",
    "card_feature_1": "Atualizações Semanais",
    "card_feature_2": "Consultas Ilimitadas",
    "card_feature_3": "IdeaForge DB com +3.000 Ideias",
    "card_feature_4": "Pesquisa Avançada com Filtros",
    "card_feature_5": "Sugestões de Funcionalidades com IA",
    "call_to_action": "Inicie Sua Jornada SaaS"
  },
  "faqSection": {
    "title": "Perguntas Frequentes",
    "sub-title": "Ainda tem dúvidas? Fale conosco por e-mail ou WhatsApp",
    "q1": "O que o IdeaForge DB oferece?",
    "r1": "O IdeaForge DB oferece acesso a um banco de dados com milhares de ideias de negócios baseadas em problemas reais discutidos por usuários de redes sociais. Você poderá filtrar as ideias por nicho, data de criação e popularidade para encontrar oportunidades validadas e economizar tempo no desenvolvimento de sua startup.",
    "q2": "O IdeaForge DB já está disponível?",
    "r2": "Estamos finalizando os detalhes do IdeaForge! Cadastre-se agora para ser um dos primeiros a acessar no lançamento e aproveite descontos exclusivos.",
    "q3": "Posso obter um reembolso?",
    "r3": "O IdeaForge DB é um produto não reembolsável. Por favor, revise os recursos e benefícios antes de adquirir. Se tiver dúvidas, entre em contato conosco.",
    "q4": "Com que frequência o IdeaForge DB é atualizado?",
    "r4": "Nosso banco de dados é atualizado semanalmente com novas ideias e tendências. Você terá acesso constante a oportunidades frescas.",
    "q5": "Que tipo de conteúdo está no IdeaForge DB?",
    "r5": "Nosso banco de dados contém ideias de negócios baseadas em problemas reais discutidos por usuários em redes sociais. Além disso, oferecemos sugestões de funcionalidades geradas por IA para ajudar você a criar soluções completas.",
    "q6": "Como acesso o IdeaForge DB após a compra?",
    "r6": "Após a compra, você receberá um e-mail com os detalhes de acesso à plataforma. Faça login para explorar o banco de dados e começar a construir sua startup."
  },
  "bottomSection": {
    "title": "Receba Ideias Inovadoras Toda Semana!",
    "sub-title": "Assine nossa newsletter e receba insights de mercado e dicas exclusivas diretamente no seu e-mail.",
    "call_to_action": "Comece Sua Jornada SaaS"
  },
  "FooterSection": {
    "text1": "Desperte Sua Criatividade com o IdeaForge",
    "text2": "© 2024 IdeaForge. Todos os direitos reservados.",
    "text3": "Desenvolvido por BeMySaaS"
  },
  "WaitlistBenefitsSection": {
    "title": "Vantagens de Participar da Lista de Espera",
    "b1": "Acesso antecipado ao nosso banco de dados de 3.000+ ideias de negócios.",
    "b2": "Um desconto especial quando lançarmos.",
    "b3": "Seja o primeiro a explorar ideias de negócios validadas e tendências.",
    "b4": "Receba atualizações sobre o desenvolvimento do produto e suas características.",
    "call_to_action": "Inicie Sua Jornada SaaS"
  },
  "EmailCaptureForm": {
    "title": "Cadastre-se na Lista de Espera",
    "alert": "Nome e e-mail são campos obrigatórios.",
    "name": "Nome",
    "email": "Email",
    "phone": "Celular (Opcional)",
    "btn": "Inscreva-se Agora",
    "msg": "Enviado com sucesso"
  },
  "HowItWorks": {
    "title": "Transforme Sua Ideia em Realidade",
    "sub-title": "A Jornada Completa para Lançar Seu Produto SaaS com Sucesso",
    "feature_title_1": "Explore um Mundo de Ideias",
    "feature_description_1": "Mergulhe em nosso extenso banco de dados com milhares de ideias de negócios inspiradas em desafios reais do mercado. Encontre a inspiração perfeita para iniciar seu projeto.",
    "feature_title_2": "Planeje com Inteligência Artificial",
    "feature_description_2": "Utilize nosso poderoso Agente de I.A. para desenvolver planos de negócios otimizados com o modelo Canvas ou Lean. Economize tempo e recursos com insights estratégicos automatizados.",
    "feature_title_3": "Crie Sua Presença Online",
    "feature_description_3": "Construa sua landing page com nossas ferramentas e templates intuitivos. Lance campanhas de marketing rapidamente com páginas personalizáveis e integração facilitada.",
    "feature_title_4": "Apoio Especializado Sempre que Precisar",
    "feature_description_4": "Conte com nosso time de especialistas para orientação em qualquer etapa do processo. Receba suporte sob medida para maximizar o potencial do seu projeto SaaS.",
    "feature_title_5": "Lançamento de Sucesso",
    "feature_description_5": "Dê vida à sua ideia e veja seu produto conquistar o mercado. Com nossa plataforma, você estará no caminho certo para alcançar o sucesso."
  },
  "TestimonialsSection": {
    "title": "O que Nossos Clientes Dizem",
    "name_1": "Ana Silva",
    "role_1": "Empreendedora",
    "text_1": "O IdeaForge DB foi uma verdadeira revolução para o meu negócio. Encontrei a ideia perfeita para minha startup e economizei meses de pesquisa. Recomendo a todos os empreendedores!",
    "name_2": "Pedro Santos",
    "role_2": "Empreendedor Digital",
    "text_2": "A plataforma IdeaForge é incrível! Encontrei uma ideia de negócio que me apaixonei e pude começar a trabalhar imediatamente. O suporte da equipe foi excepcional. Obrigado!",
    "name_3": "Mario Oliveira",
    "role_3": "Desenvolvedor de Software",
    "text_3": "O IdeaForge DB é uma ferramenta essencial para qualquer pessoa que deseja iniciar um negócio SaaS. As ideias são inovadoras e fáceis de implementar. Estou muito satisfeito com os resultados!"
  }
}

```

## messages/en.json
```json
{
  "HeaderComponent": {
    "call_to_action": "Start Your SaaS Journey Now"
  },
  "HeroComponent": {
    "hero_title_part1": "Turn Challenges",
    "hero_title_part2": "into",
    "hero_title_part3": "Successful Micro SaaS!",
    "hero_subtitle_part1": "For SaaS entrepreneurs and visionaries: Embrace the challenge and build your path with ready-made tools, validated ideas, and expert support.",
    "hero_subtitle_part2": "",
    "hero_discount": "Save $100",
    "hero_remaining": "Only 48 spots available",
    "hero_ideias_title_part1": "Access Over 3,000",
    "hero_ideias_title_part2": "Validated and Ready-to-Act Ideas",
    "call_to_action": "Start Your SaaS Journey",
    "ideas": "en"
  },
  "ValuePropositionComponent": {
    "all_in_one": "The Complete and Validated Solution for Your Business",
    "features_title_part1": "Boost Your Startup",
    "features_subtitle": "Turn real problems into micro SaaS successes with validated ideas, ready-made models, and specialized consulting.",
    "feature_title_1": "Validated Ideas",
    "feature_description_1": "Explore a comprehensive database of analyzed ideas for quick market validation and adaptation.",
    "feature_title_2": "Business Models with AI",
    "feature_description_2": "Create optimized business plans with AI, saving time and resources.",
    "feature_title_3": "Personalized Consulting",
    "feature_description_3": "Receive personalized support at every stage of development, ensuring your project's success.",
    "feature_title_4": "Integrated Tools",
    "feature_description_4": "Develop customizable pages with quick integration for marketing and launch."
  },
  "IdeaCardComponent": {
    "differentials": "Unique Differentials",
    "features": "Key Features",
    "implementation": "Ease of Implementation",
    "viability": "High Market Viability"
  },
  "FeaturesComponent": {
    "all_in_one": "The Complete and Validated Solution for Your Business",
    "features_title_part1": "Boost Your Startup with",
    "features_title_part2": "Validated Ideas!",
    "features_subtitle": "Save time and start building your SaaS with the best ideas on the market.",
    "feature_title_1": "Real Problems Database",
    "feature_description_1": "Explore business ideas based on genuine problems discussed by online communities. Focus on what matters: building a successful product.",
    "feature_title_2": "Business Ideas Database",
    "feature_description_2": "Discover untapped opportunities with AI-generated solutions, identifying market gaps and emerging trends.",
    "feature_title_3": "Constant Updates",
    "feature_description_3": "Receive new ideas weekly to stay ahead of the competition."
  },
  "PriceSection": {
    "title_part_1": "Stop Searching.",
    "title_part_2": "Start Building.",
    "card_tile_1": "Basic - Annual Access",
    "card_full_price": "$360.00",
    "card_discount_price": "$260.00",
    "card_description": "One-time payment. Create unlimited businesses with affordable plans.",
    "card_feature_1": "Weekly Updates",
    "card_feature_2": "Unlimited Queries",
    "card_feature_3": "IdeaForge DB with 3,000+ Ideas",
    "card_feature_4": "Advanced Search with Filters",
    "card_feature_5": "AI-Driven Feature Suggestions",
    "call_to_action": "Start Your SaaS Journey"
  },
  "faqSection": {
    "title": "Frequently Asked Questions",
    "sub-title": "Still have questions? Contact us via email or WhatsApp",
    "q1": "What does IdeaForge DB offer?",
    "r1": "IdeaForge DB offers access to a database with thousands of business ideas based on real problems discussed by social media users. You can filter ideas by niche, creation date, and popularity to find validated opportunities and save time on developing your startup.",
    "q2": "Is IdeaForge DB already available?",
    "r2": "We are finalizing the details of IdeaForge! Sign up now to be among the first to access it at launch and enjoy exclusive discounts.",
    "q3": "Can I get a refund?",
    "r3": "IdeaForge DB is a non-refundable product. Please review the features and benefits before purchasing. If you have any questions, contact us.",
    "q4": "How often is IdeaForge DB updated?",
    "r4": "Our database is updated weekly with new ideas and trends. You will have constant access to fresh opportunities.",
    "q5": "What type of content is in IdeaForge DB?",
    "r5": "Our database contains business ideas based on real problems discussed by social media users. We also offer AI-generated feature suggestions to help you create comprehensive solutions.",
    "q6": "How do I access IdeaForge DB after purchase?",
    "r6": "After purchase, you will receive an email with access details to the platform. Log in to explore the database and start building your startup."
  },
  "bottomSection": {
    "title": "Receive Innovative Ideas Every Week!",
    "sub-title": "Subscribe to our newsletter and receive market insights and exclusive tips directly to your email.",
    "call_to_action": "Start Your SaaS Journey"
  },
  "FooterSection": {
    "text1": "Awaken Your Creativity with IdeaForge",
    "text2": "© 2024 IdeaForge. All rights reserved.",
    "text3": "Developed by BeMySaaS"
  },
  "WaitlistBenefitsSection": {
    "title": "Benefits of Joining the Waitlist",
    "b1": "Early access to our database of 3,000+ business ideas.",
    "b2": "A special discount when we launch.",
    "b3": "Be the first to explore validated business ideas and trends.",
    "b4": "Receive updates on product development and features.",
    "call_to_action": "Start Your SaaS Journey"
  },
  "EmailCaptureForm": {
    "title": "Join the Waitlist",
    "alert": "Name and email are required fields.",
    "name": "Name",
    "email": "Email",
    "phone": "Phone (Optional)",
    "btn": "Sign Up Now",
    "msg": "Successfully sent"
  },
  "HowItWorks": {
    "title": "Turn Your Idea into Reality",
    "sub-title": "The Complete Journey to Launch Your SaaS Product Successfully",
    "feature_title_1": "Explore a World of Ideas",
    "feature_description_1": "Dive into our extensive database with thousands of business ideas inspired by real market challenges. Find the perfect inspiration to start your project.",
    "feature_title_2": "Plan with Artificial Intelligence",
    "feature_description_2": "Use our powerful AI Agent to develop optimized business plans with the Canvas or Lean model. Save time and resources with automated strategic insights.",
    "feature_title_3": "Create Your Online Presence",
    "feature_description_3": "Build your landing page with our intuitive tools and templates. Launch marketing campaigns quickly with customizable pages and seamless integration.",
    "feature_title_4": "Expert Support Whenever Needed",
    "feature_description_4": "Rely on our team of experts for guidance at any stage of the process. Receive tailored support to maximize your SaaS project's potential.",
    "feature_title_5": "Successful Launch",
    "feature_description_5": "Bring your idea to life and see your product conquer the market. With our platform, you are on the right path to achieving success."
  },
  "TestimonialsSection": {
    "title": "What Our Clients Say",
    "name_1": "Ana Silva",
    "role_1": "Entrepreneur",
    "text_1": "IdeaForge DB was a true revolution for my business. I found the perfect idea for my startup and saved months of research. I recommend it to all entrepreneurs!",
    "name_2": "Pedro Santos",
    "role_2": "Digital Entrepreneur",
    "text_2": "The IdeaForge platform is incredible! I found a business idea I was passionate about and could start working on immediately. The team support was exceptional. Thank you!",
    "name_3": "Mario Oliveira",
    "role_3": "Software Developer",
    "text_3": "IdeaForge DB is an essential tool for anyone looking to start a SaaS business. The ideas are innovative and easy to implement. I'm very satisfied with the results!"
  }
}
```

## public/hero.webp
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xc4 in position 5: invalid continuation byte
```

## public/.DS_Store
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte
```

## public/file.svg
```
<svg fill="none" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 13.5V5.41a1 1 0 0 0-.3-.7L9.8.29A1 1 0 0 0 9.08 0H1.5v13.5A2.5 2.5 0 0 0 4 16h8a2.5 2.5 0 0 0 2.5-2.5m-1.5 0v-7H8v-5H3v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1M9.5 5V2.12L12.38 5zM5.13 5h-.62v1.25h2.12V5zm-.62 3h7.12v1.25H4.5zm.62 3h-.62v1.25h7.12V11z" clip-rule="evenodd" fill="#666" fill-rule="evenodd"/></svg>
```

## public/curve-1.png.webp
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x82 in position 24: invalid start byte
```

## public/IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais.html
```html
<!DOCTYPE html>
<!-- saved from url=(0024)http://localhost:3000/pt -->
<html lang="pt" class="scroll-smooth"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><link rel="preload" as="image" imagesrcset="/_next/image?url=%2Fcurve-1.png.webp&amp;w=1200&amp;q=75 1x, /_next/image?url=%2Fcurve-1.png.webp&amp;w=3840&amp;q=75 2x"><link rel="preload" as="image" imagesrcset="/_next/image?url=%2Fhero.webp&amp;w=640&amp;q=75 1x, /_next/image?url=%2Fhero.webp&amp;w=1080&amp;q=75 2x"><link rel="preload" as="image" href="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/ai.svg"><link rel="preload" as="image" imagesrcset="/_next/image?url=%2Fcurve-3.png.webp&amp;w=640&amp;q=75 1x, /_next/image?url=%2Fcurve-3.png.webp&amp;w=1080&amp;q=75 2x"><link rel="stylesheet" href="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_[locale]_globals_7cf22d.css" data-precedence="next_static/chunks/src_app_[locale]_globals_7cf22d.css"><link rel="stylesheet" href="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/28367_react-phone-number-input_style_2fd516.css" data-precedence="next_static/chunks/28367_react-phone-number-input_style_2fd516.css"><link rel="preload" as="script" fetchpriority="low" href="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_compiled_react-dom_78920d._.js"><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_compiled_f6cecc._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_client_bc7e39._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_84105e._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/61dca_@swc_helpers_cjs_e27e0a._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/[turbopack]_browser_dev_hmr-client_hmr-client_ts_847142._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/_e69f0d._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/_16b01d._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/_2d54c0._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_favicon_ico_mjs_c51e3a._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/_f7052d._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_[locale]_layout_tsx_a54a05._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_7f8d6a._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_63c849._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/2071d_@firebase_firestore_dist_index_esm2017_23ef44.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/91d7e_libphonenumber-js_2e09f1._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/28367_react-phone-number-input_628d71._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/node_modules__pnpm_7ec9cf._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_[locale]_page_tsx_f0520a._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_[locale]_layout_tsx_a54a05(1)._.js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/2071d_@firebase_firestore_dist_index_esm2017_23ef44(1).js" async=""></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/src_app_[locale]_page_tsx_f0520a(1)._.js" async=""></script><link rel="icon" href="http://localhost:3000/favicon.ico"><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_build_polyfills_polyfill-nomodule.js" nomodule=""></script><script src="chrome-extension://mooikfkahbdckldjjndioackbalphokd/assets/prompt.js"></script><title>IdeaForge DB: Como criar Micro SaaS lucrativos resolvendo problemas reais</title><meta name="description" content="Descubra oportunidades validadas de Micro SaaS através de análise de discussões autênticas nas redes sociais. Acesse nossa base com milhares de ideias de negócios já validadas pelo mercado. Economize mais de 100 horas de pesquisa e acelere sua jornada empreendedora."><link rel="icon" href="http://localhost:3000/favicon.ico?favicon.c3478842.ico" sizes="60x70" type="image/x-icon"><meta name="viewport" content="width=device-width, initial-scale=1"></head><body class="vsc-initialized" cz-shortcut-listen="true" style=""><div><header class="bg-white py-7 border-b relative"><img alt="Curve Top Right" width="1155" height="721" decoding="async" data-nimg="1" class="absolute top-0 right-0 pointer-events-none z-auto" style="color:transparent" srcset="/_next/image?url=%2Fcurve-1.png.webp&amp;w=1200&amp;q=75 1x, /_next/image?url=%2Fcurve-1.png.webp&amp;w=3840&amp;q=75 2x" src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/curve-1.jpeg"><div class="container mx-auto flex justify-between items-center flex-col md:flex-row z-auto"><a class="text-3xl font-semibold mb-4 md:mb-0" href="http://localhost:3000/pt"><span class="text-blue-600">Idea</span>Forge</a><button class="inline-flex items-center justify-center gap-2 whitespace-nowrap font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:size-4 [&amp;_svg]:shrink-0 text-primary-foreground shadow hover:bg-primary/90 rounded-md px-3 text-xs h-16 bg-blue-600" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="radix-:R2hflt7:" data-state="closed">Inicie sua Jornada SaaS</button></div></header><section class="py-10 z-10"><div class="container mx-auto flex flex-col md:flex-row items-center gap-8"><div class="md:w-1/2"><h1 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 relative z-10 leading-tight text-center md:text-left">Transforme problemas reais<!-- --> <br> <!-- -->em<!-- --> <span class="bg-blue-600 text-white px-2 py-1 rounded leading-normal">micro SaaS de sucesso!</span></h1><p class="text-sm md:text-base text-gray-500 mb-4 md:mb-8 text-center md:text-left">Para empreendedores e visionários do SaaS: Aceite o desafio e construa seu caminho no mundo SaaS com ferramentas prontas, ideias validadas, e suporte especializado.<!-- --> <br> </p><div class="container mx-auto text-center md:text-left"><button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:size-4 [&amp;_svg]:shrink-0 text-primary-foreground shadow hover:bg-primary/90 px-4 py-2 h-16 bg-blue-600" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="radix-:R3aflt7:" data-state="closed">Inicie sua Jornada SaaS</button></div></div><div class="md:w-1/2 flex items-center justify-center z-50"><div class="max-w-md w-full aspect-video"><img alt="Ícone de IA" width="500" height="500" decoding="async" data-nimg="1" style="color:transparent" srcset="/_next/image?url=%2Fhero.webp&amp;w=640&amp;q=75 1x, /_next/image?url=%2Fhero.webp&amp;w=1080&amp;q=75 2x" src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/hero.jpeg"></div></div></div></section><section class="py-16"><div class="container mx-auto"><h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 text-gray-800 text-center">Acelere sua startup</h2><p class="text-base md:text-lg text-gray-600 mb-8 text-center">Converta problemas reais em sucessos de micro SaaS através de ideias validadas, modelos prontos e consultoria especializada.</p><div class="flex flex-col md:flex-row justify-center items-center gap-8"><div class="md:w-1/4"><div class="p-4 rounded-md"><div class="flex items-center gap-2 mb-2"><span class="rounded-full p-2 bg-yellow-500"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class="h-6 w-6 stroke-white"><path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18"></path></svg></span><h3 class="text-xl font-semibold text-gray-800">Ideias validadas</h3></div><p class="text-gray-600">Exploração de um banco abrangente de milhares de ideias analisadas para rápida validação e adaptação ao mercado.</p></div><div class="p-4 rounded-md"><div class="flex items-center gap-2 mb-2"><span class="rounded-full p-2 bg-blue-500"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-brain h-6 w-6 stroke-white"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"></path><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"></path><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"></path><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"></path><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"></path><path d="M3.477 10.896a4 4 0 0 1 .585-.396"></path><path d="M19.938 10.5a4 4 0 0 1 .585.396"></path><path d="M6 18a4 4 0 0 1-1.967-.516"></path><path d="M19.967 17.484A4 4 0 0 1 18 18"></path></svg></span><h3 class="text-xl font-semibold text-gray-800">Modelos de negócio com I.A</h3></div><p class="text-gray-600">Utilização de inteligência artificial para criar planos de negócios otimizados, economizando tempo e recursos.</p></div></div><div class="flex items-center justify-center md:w-1/4"><div class="rounded-md  p-2 text-center"><img alt="Ícone de IA" width="250" height="250" decoding="async" data-nimg="1" style="color:transparent" src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/ai.svg"></div></div><div class="md:w-1/4"><div class="p-4 rounded-md"><div class="flex items-center gap-2 mb-2"><span class="rounded-full p-2 bg-green-500"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class="h-6 w-6 stroke-white"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"></path></svg></span><h3 class="text-xl font-semibold text-gray-800">Consultoria personalizada</h3></div><p class="text-gray-600">Apoio sob medida em cada etapa do desenvolvimento, garantindo a eficácia e o sucesso do seu projeto SaaS.</p></div><div class="p-4 rounded-md"><div class="flex items-center gap-2 mb-2"><span class="rounded-full p-2 bg-gray-500"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class="h-6 w-6 stroke-white"><path stroke-linecap="round" stroke-linejoin="round" d="M14.25 6.087c0-.355.186-.676.401-.959.221-.29.349-.634.349-1.003 0-1.036-1.007-1.875-2.25-1.875s-2.25.84-2.25 1.875c0 .369.128.713.349 1.003.215.283.401.604.401.959v0a.64.64 0 0 1-.657.643 48.39 48.39 0 0 1-4.163-.3c.186 1.613.293 3.25.315 4.907a.656.656 0 0 1-.658.663v0c-.355 0-.676-.186-.959-.401a1.647 1.647 0 0 0-1.003-.349c-1.036 0-1.875 1.007-1.875 2.25s.84 2.25 1.875 2.25c.369 0 .713-.128 1.003-.349.283-.215.604-.401.959-.401v0c.31 0 .555.26.532.57a48.039 48.039 0 0 1-.642 5.056c1.518.19 3.058.309 4.616.354a.64.64 0 0 0 .657-.643v0c0-.355-.186-.676-.401-.959a1.647 1.647 0 0 1-.349-1.003c0-1.035 1.008-1.875 2.25-1.875 1.243 0 2.25.84 2.25 1.875 0 .369-.128.713-.349 1.003-.215.283-.4.604-.4.959v0c0 .333.277.599.61.58a48.1 48.1 0 0 0 5.427-.63 48.05 48.05 0 0 0 .582-4.717.532.532 0 0 0-.533-.57v0c-.355 0-.676.186-.959.401-.29.221-.634.349-1.003.349-1.035 0-1.875-1.007-1.875-2.25s.84-2.25 1.875-2.25c.37 0 .713.128 1.003.349.283.215.604.401.96.401v0a.656.656 0 0 0 .658-.663 48.422 48.422 0 0 0-.37-5.36c-1.886.342-3.81.574-5.766.689a.578.578 0 0 1-.61-.58v0Z"></path></svg></span><h3 class="text-xl font-semibold text-gray-800">Ferramentas integradas</h3></div><p class="text-gray-600">Criação de páginas personalizáveis com integração rápida para marketing e lançamento.</p></div></div></div></div></section><section class="py-16"><div class="container mx-auto"><div class="text-center mb-8"><h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-2 text-gray-800">Como Funciona</h2><p class="text-base md:text-lg text-gray-600">Descubra como nossa plataforma pode acelerar sua jornada SaaS do zero ao lançamento</p></div><div class="flex flex-col md:flex-row items-center gap-8"><div class="md:w-1/2 flex items-center justify-center z-50"><div class="max-w-md w-full aspect-video"><div class="vsc-controller"><template shadowrootmode="open">
        <style>
          @import "chrome-extension://nffaoalbilbmmfgbnbgppjihopabppdk/shadow.css";
        </style>

        <div id="controller" style="top:1385.71875px; left:343.5px; opacity:0.3">
          <span data-action="drag" class="draggable">1.00</span>
          <span id="controls">
            <button data-action="rewind" class="rw">«</button>
            <button data-action="slower">−</button>
            <button data-action="faster">+</button>
            <button data-action="advance" class="rw">»</button>
            <button data-action="display" class="hideButton">×</button>
          </span>
        </div>
      </template></div><video src="/video-demo.mp4" autoplay="" loop="" muted="" class="w-full rounded-lg"></video></div></div><div class="md:w-1/2"><div class="flex items-start gap-4 mb-6"><div style="display: inline-flex; align-items: flex-start; justify-content: flex-start;"><span class="rounded-full flex items-center justify-center text-white font-semibold text-sm bg-yellow-500" style="width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;">1</span></div><div><h3 class="text-lg font-semibold text-gray-800">Acesse milhares de ideias no nosso banco de dados</h3><p class="text-gray-600 text-sm">Explore uma vasta coleção de ideias de negócios baseadas em problemas reais.</p></div></div><div class="flex items-start gap-4 mb-6"><div style="display: inline-flex; align-items: flex-start; justify-content: flex-start;"><span class="rounded-full flex items-center justify-center text-white font-semibold text-sm bg-blue-500" style="width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;">2</span></div><div><h3 class="text-lg font-semibold text-gray-800">Utilize nosso Agente I.A para criar seu plano de negócio Canas / Lean</h3><p class="text-gray-600 text-sm">Use a inteligência artificial para gerar planos de negócios otimizados e economizar tempo e recursos.</p></div></div><div class="flex items-start gap-4 mb-6"><div style="display: inline-flex; align-items: flex-start; justify-content: flex-start;"><span class="rounded-full flex items-center justify-center text-white font-semibold text-sm bg-gray-500" style="width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;">3</span></div><div><h3 class="text-lg font-semibold text-gray-800">Construa sua LandPage com nossas ferramentas e templates</h3><p class="text-gray-600 text-sm">Crie páginas personalizáveis com integração rápida para marketing e lançamento.</p></div></div><div class="flex items-start gap-4 mb-6"><div style="display: inline-flex; align-items: flex-start; justify-content: flex-start;"><span class="rounded-full flex items-center justify-center text-white font-semibold text-sm bg-green-500" style="width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;">4</span></div><div><h3 class="text-lg font-semibold text-gray-800">Precisa de Suporte, acione nosso time de especialista para auxiliar em qualquer etapa do processo</h3><p class="text-gray-600 text-sm">Apoio sob medida em cada etapa do desenvolvimento, garantindo a eficácia e o sucesso do seu projeto SaaS.</p></div></div><div class="flex items-start gap-4 mb-6"><div style="display: inline-flex; align-items: flex-start; justify-content: flex-start;"><span class="rounded-full flex items-center justify-center text-white font-semibold text-sm bg-red-500" style="width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center;">5</span></div><div><h3 class="text-lg font-semibold text-gray-800">Seu produto lançado com sucesso!</h3><p class="text-gray-600 text-sm">Veja sua ideia ganhar vida e comece a trilhar seu caminho para o sucesso.</p></div></div></div></div></div></section><div class="w-full max-w-3xl p-2 mx-auto rounded-2xl"><img alt="Curve Left" width="470" height="928" decoding="async" data-nimg="1" class="absolute top-0 right-0 z-0 pointer-events-none" style="color:transparent" srcset="/_next/image?url=%2Fcurve-3.png.webp&amp;w=640&amp;q=75 1x, /_next/image?url=%2Fcurve-3.png.webp&amp;w=1080&amp;q=75 2x" src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/curve-3.jpeg"><div class="container mx-auto"><h2 class="text-2xl md:text-3xl lg:text-5xl font-bold mb-4 text-center">Perguntas Frequentes</h2><p class="text-base md:text-lg text-gray-500 mb-4 md:mb-8 text-center">Tem mais dúvidas? Entre em contato por e-mail ou WhatsApp<!-- --> <br><span class="text-blue-500"><a href="https://api.whatsapp.com/send?phone=5534988542408&amp;text=I%20am%20interested%20in%20IdeaForge%20DB%20and%20would%20like%20to%20ask%20some%20questions." target="_blank">WhatsApp</a></span></p></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R4tflt7:" aria-expanded="false" data-headlessui-state=""><span>O que o IdeaForge DB oferece?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R55flt7:" aria-expanded="false" data-headlessui-state=""><span>O IdeaForge DB já está disponível?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R5dflt7:" aria-expanded="false" data-headlessui-state=""><span>Posso obter um reembolso?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R5lflt7:" aria-expanded="false" data-headlessui-state=""><span>Com que frequência o IdeaForge DB é atualizado?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R5tflt7:" aria-expanded="false" data-headlessui-state=""><span>Que tipo de conteúdo está no IdeaForge DB?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><div class="mb-5"><div data-headlessui-state=""><div class="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200" id="headlessui-disclosure-button-:R65flt7:" aria-expanded="false" data-headlessui-state=""><span>Como acesso o IdeaForge DB após a compra?</span><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" class=" w-5 h-5 text-indigo-500"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5"></path></svg></div></div></div><br><br></div><section class="bg-blue-600 py-16 text-white text-center"><div class="container mx-auto px-4"> <h2 class="text-2xl md:text-3xl lg:text-5xl font-bold mb-4 ml-4 mr-4">Receba Ideias Novas Toda Semana!</h2><p class="text-base md:text-lg mb-8 md:mb-8 text-center">Assine nossa newsletter e descubra semanalmente ideias inovadoras, insights de mercado e dicas exclusivas diretamente no seu e-mail.</p><form class="flex flex-col md:flex-row items-center justify-center gap-4" action="javascript:throw new Error(&#39;A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\&#39;re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().&#39;)"><div class="relative w-full md:w-auto"><input type="email" class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm text-white placeholder:text-white placeholder-opacity-70 pr-10 md:w-64" placeholder="Seu e-mail" required="" name="email"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-mail absolute right-3 top-2.5 h-5 w-5 text-white pointer-events-none"><rect width="20" height="16" x="2" y="4" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg></div><button class="inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&amp;_svg]:pointer-events-none [&amp;_svg]:size-4 [&amp;_svg]:shrink-0 bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80 h-10 rounded-md px-8" type="submit">Inicie sua Jornada SaaS</button></form></div></section><footer class="bg-white border-t py-8"><div class="container mx-auto flex flex-col md:flex-row justify-between items-center text-center md:text-left"><div class="mb-4 md:mb-0"><a class="text-xl font-semibold flex items-center" href="http://localhost:3000/"><span class="text-blue-600">Idea</span>Forge</a><p class="text-gray-500 text-sm">Desperte sua criatividade.</p></div><div class="text-center md:text-right"><p class="text-gray-500 text-sm mb-2">© 2024 IdeaForge. Todos os direitos reservados.</p><div class="flex items-center justify-center md:justify-end"><span class="text-blue-600">Idea</span>Forge<p class="text-gray-500 ml-1 text-sm">IdeaForge Construído por BeMySaaS</p></div></div></div></footer></div><script>addEventListener("submit",function(a){if(!a.defaultPrevented){var c=a.target,d=a.submitter,e=c.action,b=d;if(d){var f=d.getAttribute("formAction");null!=f&&(e=f,b=null)}"javascript:throw new Error('React form unexpectedly submitted.')"===e&&(a.preventDefault(),b?(a=document.createElement("input"),a.name=b.name,a.value=b.value,b.parentNode.insertBefore(a,b),b=new FormData(c),a.parentNode.removeChild(a)):b=new FormData(c),a=c.ownerDocument||c,(a.$$reactFormReplay=a.$$reactFormReplay||[]).push(c,d,b))}});</script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/c488b_next_dist_compiled_react-dom_78920d._.js" async=""></script><script>(self.__next_f=self.__next_f||[]).push([0])</script><script>self.__next_f.push([1,"3:\"$Sreact.fragment\"\n4:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/components/layout-router.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"default\"]\n5:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/components/render-from-template-context.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"default\"]\nb:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/components/client-page.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"ClientPageRoot\"]\nc:I[\"[project]/src/app/[locale]/page.tsx [app-client] (ecmascript)\",[\"static/chunks/_f7052d._.js\",\"static/chunks/src_app_[locale]_layout_tsx_a54a05._.js\",\"static/chunks/src_7f8d6a._.js\",\"static/chunks/c488b_next_63c849._.js\",\"static/chunks/2071d_@firebase_firestore_dist_index_esm2017_23ef44.js\",\"static/chunks/91d7e_libphonenumber-js_2e09f1._.js\",\"static/chunks/28367_react-phone-number-input_628d71._.js\",\"static/chunks/node_modules__pnpm_7ec9cf._.js\",\"static/chunks/src_app_[locale]_page_tsx_f0520a._.js\"],\"default\"]\nd:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/lib/metadata/metadata-boundary.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"OutletBoundary\"]\n11:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/components/client-segment.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"ClientSegmentRoot\"]\n12:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/com"])</script><script>self.__next_f.push([1,"ponents/error-boundary.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"default\"]\n13:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/client/components/http-access-fallback/error-boundary.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"HTTPAccessFallbackBoundary\"]\n14:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/lib/metadata/metadata-boundary.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"MetadataBoundary\"]\n15:I[\"[project]/node_modules/.pnpm/next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0/node_modules/next/dist/lib/metadata/metadata-boundary.js [app-client] (ecmascript)\",[\"static/chunks/_2d54c0._.js\",\"static/chunks/src_app_favicon_ico_mjs_c51e3a._.js\"],\"ViewportBoundary\"]\n16:\"$SkResourceStore\"\n:HL[\"/_next/static/chunks/src_app_%5Blocale%5D_globals_7cf22d.css\",\"style\"]\n:HL[\"/_next/static/chunks/28367_react-phone-number-input_style_2fd516.css\",\"style\"]\n2:{\"name\":\"Preloads\",\"env\":\"Server\",\"key\":null,\"owner\":null,\"props\":{\"preloadCallbacks\":[\"$E(()=\u003e{ctx.componentMod.preloadStyle(fullHref,ctx.renderOpts.crossOrigin,ctx.nonce)})\",\"$E(()=\u003e{ctx.componentMod.preloadStyle(fullHref,ctx.renderOpts.crossOrigin,ctx.nonce)})\"]}}\n1:D\"$2\"\n1:null\n7:{\"name\":\"NotFound\",\"env\":\"Server\",\"key\":null,\"owner\":null,\"props\":{}}\n6:D\"$7\"\n8:{\"name\":\"HTTPAccessErrorFallback\",\"env\":\"Server\",\"key\":null,\"owner\":\"$7\",\"props\":{\"status\":404,\"message\":\"This page could not be found.\"}}\n6:D\"$8\"\n6:[[\"$\",\"title\",null,{\"children\":\"404: This page could not be found.\"},\"$8\"],[\"$\",\"div\",null,{\"style\":{\"fontFamily\":\"system-ui,\\\"Segoe UI\\\",Roboto,Helvetica,Arial,sans-serif,\\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\"\",\"height\":\"100vh\",\"textAlign\":\"center\",\"display\":\"flex\",\"flexDirection\":\"column\",\"alignItems\":\"center\",\"justifyContent\":\"ce"])</script><script>self.__next_f.push([1,"nter\"},\"children\":[\"$\",\"div\",null,{\"children\":[[\"$\",\"style\",null,{\"dangerouslySetInnerHTML\":{\"__html\":\"body{color:#000;background:#fff;margin:0}.next-error-h1{border-right:1px solid rgba(0,0,0,.3)}@media (prefers-color-scheme:dark){body{color:#fff;background:#000}.next-error-h1{border-right:1px solid rgba(255,255,255,.3)}}\"}},\"$8\"],[\"$\",\"h1\",null,{\"className\":\"next-error-h1\",\"style\":{\"display\":\"inline-block\",\"margin\":\"0 20px 0 0\",\"padding\":\"0 23px 0 0\",\"fontSize\":24,\"fontWeight\":500,\"verticalAlign\":\"top\",\"lineHeight\":\"49px\"},\"children\":404},\"$8\"],[\"$\",\"div\",null,{\"style\":{\"display\":\"inline-block\"},\"children\":[\"$\",\"h2\",null,{\"style\":{\"fontSize\":14,\"fontWeight\":400,\"lineHeight\":\"49px\",\"margin\":0},\"children\":\"This page could not be found.\"},\"$8\"]},\"$8\"]]},\"$8\"]},\"$8\"]]\na:{\"name\":\"LocaleLayout\",\"env\":\"Server\",\"key\":null,\"owner\":null,\"props\":{\"children\":[\"$\",\"$L4\",null,{\"parallelRouterKey\":\"children\",\"segmentPath\":[\"children\",\"$0:f:0:1:2:children:0\",\"children\"],\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$3\",null,{\"children\":[\"$\",\"$L5\",null,{},null]},null],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":\"$undefined\",\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"},null],\"params\":\"$@\"}}\n9:D\"$a\"\nf:{\"name\":\"__next_outlet_boundary__\",\"env\":\"Server\",\"key\":null,\"owner\":null,\"props\":{\"ready\":\"$E(async function getMetadataAndViewportReady() {\\n        await viewport();\\n        await metadata();\\n        return undefined;\\n    })\"}}\ne:D\"$f\"\n"])</script><script>self.__next_f.push([1,"17:{\"name\":\"NonIndex\",\"env\":\"Server\",\"key\":null,\"owner\":null,\"props\":{\"ctx\":{\"componentMod\":{\"ClientPageRoot\":\"$b\",\"ClientSegmentRoot\":\"$11\",\"GlobalError\":\"$12\",\"HTTPAccessFallbackBoundary\":\"$13\",\"LayoutRouter\":\"$4\",\"MetadataBoundary\":\"$14\",\"OutletBoundary\":\"$d\",\"Postpone\":\"$E(function Postpone({ reason, route }) {\\n    const prerenderStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    const dynamicTracking = prerenderStore \u0026\u0026 prerenderStore.type === 'prerender-ppr' ? prerenderStore.dynamicTracking : null;\\n    postponeWithTracking(route, reason, dynamicTracking);\\n})\",\"RenderFromTemplateContext\":\"$5\",\"ViewportBoundary\":\"$15\",\"__next_app__\":{\"require\":\"$E(function () { [native code] })\",\"loadChunk\":\"$E(function () { [native code] })\"},\"actionAsyncStorage\":{\"kResourceStore\":\"$16\",\"enabled\":true},\"collectSegmentData\":\"$E(async function collectSegmentData(fullPageDataBuffer, staleTime, clientModules, serverConsumerManifest) {\\n    // Traverse the router tree and generate a prefetch response for each segment.\\n    // A mutable map to collect the results as we traverse the route tree.\\n    const resultMap = new Map();\\n    // Before we start, warm up the module cache by decoding the page data once.\\n    // Then we can assume that any remaining async tasks that occur the next time\\n    // are due to hanging promises caused by dynamic data access. Note we only\\n    // have to do this once per page, not per individual segment.\\n    //\\n    try {\\n        await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2d$server$2d$dom$2d$turbopack$2f$client$2e$edge$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"createFromReadableStream\\\"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$stream$2d$utils$2f$node$2d$web$2d$streams$2d$helper$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"streamFromBuffer\\\"])(fullPageDataBuffer), {\\n            serverConsumerManifest\\n        });\\n        await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$lib$2f$scheduler$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"waitAtLeastOneReactRenderTask\\\"])();\\n    } catch  {}\\n    // Create an abort controller that we'll use to stop the stream.\\n    const abortController = new AbortController();\\n    const onCompletedProcessingRouteTree = async ()=\u003e{\\n        // Since all we're doing is decoding and re-encoding a cached prerender, if\\n        // serializing the stream takes longer than a microtask, it must because of\\n        // hanging promises caused by dynamic data.\\n        await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$lib$2f$scheduler$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"waitAtLeastOneReactRenderTask\\\"])();\\n        abortController.abort();\\n    };\\n    // Generate a stream for the route tree prefetch. While we're walking the\\n    // tree, we'll also spawn additional tasks to generate the segment prefetches.\\n    // The promises for these tasks are pushed to a mutable array that we will\\n    // await once the route tree is fully rendered.\\n    const segmentTasks = [];\\n    const { prelude: treeStream } = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$static$2d$edge$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"prerender\\\"])(// we need to use a component so that when we decode the original stream\\n    // inside of it, the side effects are transferred to the new stream.\\n    // @ts-expect-error\\n    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(PrefetchTreeData, {\\n        fullPageDataBuffer: fullPageDataBuffer,\\n        serverConsumerManifest: serverConsumerManifest,\\n        clientModules: clientModules,\\n        staleTime: staleTime,\\n        segmentTasks: segmentTasks,\\n        onCompletedProcessingRouteTree: onCompletedProcessingRouteTree\\n    }), clientModules, {\\n        signal: abortController.signal,\\n        onError () {\\n        // Ignore any errors. These would have already been reported when\\n        // we created the full page data.\\n        }\\n    });\\n    // Write the route tree to a special `/_tree` segment.\\n    const treeBuffer = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$stream$2d$utils$2f$node$2d$web$2d$streams$2d$helper$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"streamToBuffer\\\"])(treeStream);\\n    resultMap.set('/_tree', treeBuffer);\\n    // Now that we've finished rendering the route tree, all the segment tasks\\n    // should have been spawned. Await them in parallel and write the segment\\n    // prefetches to the result map.\\n    for (const [segmentPath, buffer] of (await Promise.all(segmentTasks))){\\n        resultMap.set(segmentPath, buffer);\\n    }\\n    return resultMap;\\n})\",\"createMetadataComponents\":\"$E(function createMetadataComponents({ tree, searchParams, metadataContext, getDynamicParamFromSegment, appUsingSizeAdjustment, errorType, createServerParamsForMetadata, workStore, MetadataBoundary, ViewportBoundary }) {\\n    function MetadataRoot() {\\n        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsxs\\\"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"Fragment\\\"], {\\n            children: [\\n                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(MetadataBoundary, {\\n                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(Metadata, {})\\n                }),\\n                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(ViewportBoundary, {\\n                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(Viewport, {})\\n                }),\\n                appUsingSizeAdjustment ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"jsx\\\"])(\\\"meta\\\", {\\n                    name: \\\"next-size-adjust\\\",\\n                    content: \\\"\\\"\\n                }) : null\\n            ]\\n        });\\n    }\\n    async function viewport() {\\n        return getResolvedViewport(tree, searchParams, getDynamicParamFromSegment, createServerParamsForMetadata, workStore, errorType);\\n    }\\n    async function Viewport() {\\n        try {\\n            return await viewport();\\n        } catch (error) {\\n            if (!errorType \u0026\u0026 (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$client$2f$components$2f$http$2d$access$2d$fallback$2f$http$2d$access$2d$fallback$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"isHTTPAccessFallbackError\\\"])(error)) {\\n                try {\\n                    return await getNotFoundViewport(tree, searchParams, getDynamicParamFromSegment, createServerParamsForMetadata, workStore);\\n                } catch  {}\\n            }\\n            // We don't actually want to error in this component. We will\\n            // also error in the MetadataOutlet which causes the error to\\n            // bubble from the right position in the page to be caught by the\\n            // appropriate boundaries\\n            return null;\\n        }\\n    }\\n    Viewport.displayName = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$lib$2f$metadata$2f$metadata$2d$constants$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"VIEWPORT_BOUNDARY_NAME\\\"];\\n    async function metadata() {\\n        return getResolvedMetadata(tree, searchParams, getDynamicParamFromSegment, metadataContext, createServerParamsForMetadata, workStore, errorType);\\n    }\\n    async function Metadata() {\\n        try {\\n            return await metadata();\\n        } catch (error) {\\n            if (!errorType \u0026\u0026 (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$client$2f$components$2f$http$2d$access$2d$fallback$2f$http$2d$access$2d$fallback$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"isHTTPAccessFallbackError\\\"])(error)) {\\n                try {\\n                    return await getNotFoundMetadata(tree, searchParams, getDynamicParamFromSegment, metadataContext, createServerParamsForMetadata, workStore);\\n                } catch  {}\\n            }\\n            // We don't actually want to error in this component. We will\\n            // also error in the MetadataOutlet which causes the error to\\n            // bubble from the right position in the page to be caught by the\\n            // appropriate boundaries\\n            return null;\\n        }\\n    }\\n    Metadata.displayName = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$lib$2f$metadata$2f$metadata$2d$constants$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"METADATA_BOUNDARY_NAME\\\"];\\n    async function getMetadataAndViewportReady() {\\n        await viewport();\\n        await metadata();\\n        return undefined;\\n    }\\n    return [\\n        MetadataRoot,\\n        getMetadataAndViewportReady\\n    ];\\n})\",\"createPrerenderParamsForClientSegment\":\"$E(function createPrerenderParamsForClientSegment(underlyingParams, workStore) {\\n    const prerenderStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (prerenderStore \u0026\u0026 prerenderStore.type === 'prerender') {\\n        const fallbackParams = workStore.fallbackRouteParams;\\n        if (fallbackParams) {\\n            for(let key in underlyingParams){\\n                if (fallbackParams.has(key)) {\\n                    // This params object has one of more fallback params so we need to consider\\n                    // the awaiting of this params object \\\"dynamic\\\". Since we are in dynamicIO mode\\n                    // we encode this as a promise that never resolves\\n                    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$dynamic$2d$rendering$2d$utils$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"makeHangingPromise\\\"])(prerenderStore.renderSignal, '`params`');\\n                }\\n            }\\n        }\\n    }\\n    // We're prerendering in a mode that does not abort. We resolve the promise without\\n    // any tracking because we're just transporting a value from server to client where the tracking\\n    // will be applied.\\n    return Promise.resolve(underlyingParams);\\n})\",\"createPrerenderSearchParamsForClientPage\":\"$E(function createPrerenderSearchParamsForClientPage(workStore) {\\n    if (workStore.forceStatic) {\\n        // When using forceStatic we override all other logic and always just return an empty\\n        // dictionary object.\\n        return Promise.resolve({});\\n    }\\n    const prerenderStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (prerenderStore \u0026\u0026 prerenderStore.type === 'prerender') {\\n        // dynamicIO Prerender\\n        // We're prerendering in a mode that aborts (dynamicIO) and should stall\\n        // the promise to ensure the RSC side is considered dynamic\\n        return (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$dynamic$2d$rendering$2d$utils$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"makeHangingPromise\\\"])(prerenderStore.renderSignal, '`searchParams`');\\n    }\\n    // We're prerendering in a mode that does not aborts. We resolve the promise without\\n    // any tracking because we're just transporting a value from server to client where the tracking\\n    // will be applied.\\n    return Promise.resolve({});\\n})\",\"createServerParamsForMetadata\":\"$E(function createServerParamsForServerSegment(underlyingParams, workStore) {\\n    const workUnitStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (workUnitStore) {\\n        switch(workUnitStore.type){\\n            case 'prerender':\\n            case 'prerender-ppr':\\n            case 'prerender-legacy':\\n                return createPrerenderParams(underlyingParams, workStore, workUnitStore);\\n            default:\\n        }\\n    }\\n    return createRenderParams(underlyingParams, workStore);\\n})\",\"createServerParamsForServerSegment\":\"$E(function createServerParamsForServerSegment(underlyingParams, workStore) {\\n    const workUnitStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (workUnitStore) {\\n        switch(workUnitStore.type){\\n            case 'prerender':\\n            case 'prerender-ppr':\\n            case 'prerender-legacy':\\n                return createPrerenderParams(underlyingParams, workStore, workUnitStore);\\n            default:\\n        }\\n    }\\n    return createRenderParams(underlyingParams, workStore);\\n})\",\"createServerSearchParamsForMetadata\":\"$E(function createServerSearchParamsForServerPage(underlyingSearchParams, workStore) {\\n    const workUnitStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (workUnitStore) {\\n        switch(workUnitStore.type){\\n            case 'prerender':\\n            case 'prerender-ppr':\\n            case 'prerender-legacy':\\n                return createPrerenderSearchParams(workStore, workUnitStore);\\n            default:\\n        }\\n    }\\n    return createRenderSearchParams(underlyingSearchParams, workStore);\\n})\",\"createServerSearchParamsForServerPage\":\"$E(function createServerSearchParamsForServerPage(underlyingSearchParams, workStore) {\\n    const workUnitStore = __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"].getStore();\\n    if (workUnitStore) {\\n        switch(workUnitStore.type){\\n            case 'prerender':\\n            case 'prerender-ppr':\\n            case 'prerender-legacy':\\n                return createPrerenderSearchParams(workStore, workUnitStore);\\n            default:\\n        }\\n    }\\n    return createRenderSearchParams(underlyingSearchParams, workStore);\\n})\",\"createTemporaryReferenceSet\":\"$E(function(){return new WeakMap})\",\"decodeAction\":\"$E(function(body,serverManifest){var formData=new FormData,action=null;return body.forEach(function(value1,key){key.startsWith(\\\"$ACTION_\\\")?key.startsWith(\\\"$ACTION_REF_\\\")?(value1=decodeBoundActionMetaData(body,serverManifest,value1=\\\"$ACTION_\\\"+key.slice(12)+\\\":\\\"),action=loadServerReference(serverManifest,value1.id,value1.bound)):key.startsWith(\\\"$ACTION_ID_\\\")\u0026\u0026(action=loadServerReference(serverManifest,value1=key.slice(11),null)):formData.append(key,value1)}),null===action?null:action.then(function(fn){return fn.bind(null,formData)})})\",\"decodeFormState\":\"$E(function(actionResult,body,serverManifest){var keyPath=body.get(\\\"$ACTION_KEY\\\");if(\\\"string\\\"!=typeof keyPath)return Promise.resolve(null);var metaData=null;if(body.forEach(function(value1,key){key.startsWith(\\\"$ACTION_REF_\\\")\u0026\u0026(metaData=decodeBoundActionMetaData(body,serverManifest,\\\"$ACTION_\\\"+key.slice(12)+\\\":\\\"))}),null===metaData)return Promise.resolve(null);var referenceId=metaData.id;return Promise.resolve(metaData.bound).then(function(bound){return null===bound?null:[actionResult,keyPath,referenceId,bound.length-1]})})\",\"decodeReply\":\"$E(function(body,turbopackMap,options){if(\\\"string\\\"==typeof body){var form=new FormData;form.append(\\\"0\\\",body),body=form}return turbopackMap=getChunk(body=createResponse(turbopackMap,\\\"\\\",options?options.temporaryReferences:void 0,body),0),close(body),turbopackMap})\",\"pages\":[\"[project]/src/app/[locale]/page.tsx\"],\"patchFetch\":\"$E(function patchFetch() {\\n    return (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$esm$2f$server$2f$lib$2f$patch$2d$fetch$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"patchFetch\\\"])({\\n        workAsyncStorage: __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workAsyncStorage\\\"],\\n        workUnitAsyncStorage: __TURBOPACK__imported__module__$5b$externals$5d2f$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js__$5b$external$5d$__$28$next$2f$dist$2f$server$2f$app$2d$render$2f$work$2d$unit$2d$async$2d$storage$2e$external$2e$js$2c$__cjs$29$__[\\\"workUnitAsyncStorage\\\"]\\n    });\\n})\",\"preconnect\":\"$E(function preconnect(href, crossOrigin, nonce) {\\n    const opts = {};\\n    if (typeof crossOrigin === 'string') {\\n        opts.crossOrigin = crossOrigin;\\n    }\\n    if (typeof nonce === 'string') {\\n        opts.nonce = nonce;\\n    }\\n    ;\\n    __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$dom$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"default\\\"].preconnect(href, opts);\\n})\",\"preloadFont\":\"$E(function preloadFont(href, type, crossOrigin, nonce) {\\n    const opts = {\\n        as: 'font',\\n        type\\n    };\\n    if (typeof crossOrigin === 'string') {\\n        opts.crossOrigin = crossOrigin;\\n    }\\n    if (typeof nonce === 'string') {\\n        opts.nonce = nonce;\\n    }\\n    __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$dom$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"default\\\"].preload(href, opts);\\n})\",\"preloadStyle\":\"$E(function preloadStyle(href, crossOrigin, nonce) {\\n    const opts = {\\n        as: 'style'\\n    };\\n    if (typeof crossOrigin === 'string') {\\n        opts.crossOrigin = crossOrigin;\\n    }\\n    if (typeof nonce === 'string') {\\n        opts.nonce = nonce;\\n    }\\n    __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f2e$pnpm$2f$next$40$15$2e$1$2e$4_react$2d$dom$40$19$2e$0$2e$0_react$40$19$2e$0$2e$0_$5f$react$40$19$2e$0$2e$0$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$dom$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__[\\\"default\\\"].preload(href, opts);\\n})\",\"prerender\":\"$undefined\",\"renderToReadableStream\":\"$E(function(model,turbopackMap,options){var request=new RequestInstance(20,model,turbopackMap,options?options.onError:void 0,options?options.identifierPrefix:void 0,options?options.onPostpone:void 0,options?options.temporaryReferences:void 0,options?options.environmentName:void 0,options?options.filterStackFrame:void 0,noop,noop);if(options\u0026\u0026options.signal){var signal=options.signal;if(signal.aborted)abort(request,signal.reason);else{var listener=function(){abort(request,signal.reason),signal.removeEventListener(\\\"abort\\\",listener)};signal.addEventListener(\\\"abort\\\",listener)}}return new ReadableStream({type:\\\"bytes\\\",start:function(){request.flushScheduled=null!==request.destination,supportsRequestStorage?scheduleMicrotask(function(){requestStorage.run(request,performWork,request)}):scheduleMicrotask(function(){return performWork(request)}),setTimeoutOrImmediate(function(){request.status===OPENING\u0026\u0026(request.status=11)},0)},pull:function(controller){if(request.status===CLOSING)request.status=CLOSED,closeWithError(controller,request.fatalError);else if(request.status!==CLOSED\u0026\u0026null===request.destination){request.destination=controller;try{flushCompletedChunks(request,controller)}catch(error){logRecoverableError(request,error,null),fatalError(request,error)}}},cancel:function(reason){request.destination=null,abort(request,reason)}},{highWaterMark:0})})\",\"routeModule\":{\"userland\":{\"loaderTree\":[\"\",\"$Y\",\"$Y\"]},\"definition\":\"$Y\"},\"serverHooks\":\"$Y\",\"taintObjectReference\":\"$E(function notImplemented() {\\n    throw new Error('Taint can only be used with the taint flag.');\\n})\",\"tree\":\"$Y\",\"workAsyncStorage\":\"$Y\",\"workUnitAsyncStorage\":\"$Y\"},\"url\":\"$Y\",\"renderOpts\":\"$Y\",\"workStore\":\"$Y\",\"parsedRequestHeaders\":\"$Y\",\"getDynamicParamFromSegment\":\"$E(function(segment){let segmentParam=getSegmentParam(segment);if(!segmentParam)return null;let key=segmentParam.param,value1=params[key];if(fallbackRouteParams\u0026\u0026fallbackRouteParams.has(segmentParam.param)?value1=fallbackRouteParams.get(segmentParam.param):Array.isArray(value1)?value1=value1.map(i=\u003eencodeURIComponent(i)):\\\"string\\\"==typeof value1\u0026\u0026(value1=encodeURIComponent(value1)),!value1){let isCatchall=\\\"catchall\\\"===segmentParam.type,isOptionalCatchall=\\\"optional-catchall\\\"===segmentParam.type;if(isCatchall||isOptionalCatchall){let dynamicParamType=dynamicParamTypes[segmentParam.type];return isOptionalCatchall?{param:key,value:null,type:dynamicParamType,treeSegment:[key,\\\"\\\",dynamicParamType]}:{param:key,value:value1=pagePath.split(\\\"/\\\").slice(1).flatMap(pathSegment=\u003e{let param=function(param){let match=param.match(PARAMETER_PATTERN);return match?parseMatchedParameter(match[1]):parseMatchedParameter(param)}(pathSegment);return params[param.key]??param.key}),type:dynamicParamType,treeSegment:[key,value1.join(\\\"/\\\"),dynamicParamType]}}}let type=function(type){let short=dynamicParamTypes[type];if(!short)throw Error(\\\"Unknown dynamic param type\\\");return short}(segmentParam.type);return{param:key,value:value1,treeSegment:[key,Array.isArray(value1)?value1.join(\\\"/\\\"):value1,type],type:type}})\",\"query\":\"$0:f:0:1:2:children:2:children:1:props:children:0:props:searchParams\",\"isPrefetch\":false,\"isAction\":false,\"requestTimestamp\":1736710689305,\"appUsingSizeAdjustment\":false,\"flightRouterState\":\"$undefined\",\"requestId\":\"dGZSFoCrhfjounFX9l_s3\",\"pagePath\":\"/[locale]\",\"clientReferenceManifest\":\"$Y\",\"assetPrefix\":\"\",\"isNotFoundPath\":false,\"nonce\":\"$undefined\",\"res\":\"$Y\"}}}\n"])</script><script>self.__next_f.push([1,"10:D\"$17\"\n10:null\n19:{\"name\":\"MetadataRoot\",\"env\":\"Server\",\"key\":\"dGZSFoCrhfjounFX9l_s3\",\"owner\":null,\"props\":{}}\n18:D\"$19\"\n1b:{\"name\":\"__next_metadata_boundary__\",\"env\":\"Server\",\"key\":null,\"owner\":\"$19\",\"props\":{}}\n1a:D\"$1b\"\n1d:{\"name\":\"__next_viewport_boundary__\",\"env\":\"Server\",\"key\":null,\"owner\":\"$19\",\"props\":{}}\n1c:D\"$1d\"\n18:[\"$\",\"$3\",\"dGZSFoCrhfjounFX9l_s3\",{\"children\":[[\"$\",\"$L14\",null,{\"children\":\"$L1a\"},\"$19\"],[\"$\",\"$L15\",null,{\"children\":\"$L1c\"},\"$19\"],null]},null]\n1e:[]\n"])</script><script>self.__next_f.push([1,"0:{\"P\":\"$1\",\"b\":\"development\",\"p\":\"\",\"c\":[\"\",\"pt\"],\"i\":false,\"f\":[[[\"\",{\"children\":[[\"locale\",\"pt\",\"d\"],{\"children\":[\"__PAGE__\",{}]},\"$undefined\",\"$undefined\",true]}],[\"\",[\"$\",\"$3\",\"c\",{\"children\":[null,[\"$\",\"$L4\",null,{\"parallelRouterKey\":\"children\",\"segmentPath\":[\"children\"],\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L5\",null,{},null],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":[[],\"$6\"],\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"},null]]},null],{\"children\":[[\"locale\",\"pt\",\"d\"],[\"$\",\"$3\",\"c\",{\"children\":[[[\"$\",\"link\",\"0\",{\"rel\":\"stylesheet\",\"href\":\"/_next/static/chunks/src_app_%5Blocale%5D_globals_7cf22d.css\",\"precedence\":\"next_static/chunks/src_app_[locale]_globals_7cf22d.css\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-0\",{\"src\":\"/_next/static/chunks/_f7052d._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-1\",{\"src\":\"/_next/static/chunks/src_app_%5Blocale%5D_layout_tsx_a54a05._.js\",\"async\":true,\"nonce\":\"$undefined\"},null]],\"$L9\"]},null],{\"children\":[\"__PAGE__\",[\"$\",\"$3\",\"c\",{\"children\":[[\"$\",\"$Lb\",null,{\"Component\":\"$c\",\"searchParams\":{},\"params\":{\"locale\":\"pt\"}},null],[[\"$\",\"link\",\"0\",{\"rel\":\"stylesheet\",\"href\":\"/_next/static/chunks/28367_react-phone-number-input_style_2fd516.css\",\"precedence\":\"next_static/chunks/28367_react-phone-number-input_style_2fd516.css\",\"crossOrigin\":\"$undefined\",\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-0\",{\"src\":\"/_next/static/chunks/src_7f8d6a._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-1\",{\"src\":\"/_next/static/chunks/c488b_next_63c849._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-2\",{\"src\":\"/_next/static/chunks/2071d_%40firebase_firestore_dist_index_esm2017_23ef44.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-3\",{\"src\":\"/_next/static/chunks/91d7e_libphonenumber-js_2e09f1._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-4\",{\"src\":\"/_next/static/chunks/28367_react-phone-number-input_628d71._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-5\",{\"src\":\"/_next/static/chunks/node_modules__pnpm_7ec9cf._.js\",\"async\":true,\"nonce\":\"$undefined\"},null],[\"$\",\"script\",\"script-6\",{\"src\":\"/_next/static/chunks/src_app_%5Blocale%5D_page_tsx_f0520a._.js\",\"async\":true,\"nonce\":\"$undefined\"},null]],[\"$\",\"$Ld\",null,{\"children\":\"$Le\"},null]]},null],{},null,false]},null,false]},null,false],[\"$\",\"$3\",\"h\",{\"children\":[\"$10\",\"$18\"]},null],false]],\"m\":\"$W1e\",\"G\":[\"$12\",\"$undefined\"],\"s\":false,\"S\":false}\n"])</script><script>self.__next_f.push([1,"1c:[[\"$\",\"meta\",\"0\",{\"name\":\"viewport\",\"content\":\"width=device-width, initial-scale=1\"},\"$f\"]]\n1a:[[\"$\",\"meta\",\"0\",{\"charSet\":\"utf-8\"},\"$1b\"],[\"$\",\"title\",\"1\",{\"children\":\"IdeaForge DB: Como criar Micro SaaS lucrativos resolvendo problemas reais\"},\"$1b\"],[\"$\",\"meta\",\"2\",{\"name\":\"description\",\"content\":\"Descubra oportunidades validadas de Micro SaaS através de análise de discussões autênticas nas redes sociais. Acesse nossa base com milhares de ideias de negócios já validadas pelo mercado. Economize mais de 100 horas de pesquisa e acelere sua jornada empreendedora.\"},\"$1b\"],[\"$\",\"link\",\"3\",{\"rel\":\"icon\",\"href\":\"/favicon.ico?favicon.c3478842.ico\",\"sizes\":\"60x70\",\"type\":\"image/x-icon\"},\"$1b\"]]\ne:null\n"])</script><script>self.__next_f.push([1,"20:{\"name\":\"i\",\"env\":\"Server\",\"key\":null,\"owner\":\"$a\",\"props\":{\"messages\":{\"HeaderComponent\":{\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"HeroComponent\":{\"hero_title_part1\":\"Transforme problemas reais\",\"hero_title_part2\":\"em\",\"hero_title_part3\":\"micro SaaS de sucesso!\",\"hero_subtitle_part1\":\"Para empreendedores e visionários do SaaS: Aceite o desafio e construa seu caminho no mundo SaaS com ferramentas prontas, ideias validadas, e suporte especializado.\",\"hero_subtitle_part2\":\"\",\"hero_discount\":\"R$100 de desconto\",\"hero_remaining\":\"48 vagas restantes\",\"hero_ideias_title_part1\":\"Acesse mais de 3000 ideias\",\"hero_ideias_title_part2\":\"validadas e prontas para ação\",\"call_to_action\":\"Inicie sua Jornada SaaS\",\"ideas\":\"pt\"},\"ValuePropositionComponent\":{\"all_in_one\":\"Solução completa e validada\",\"features_title_part1\":\"Acelere sua startup\",\"features_subtitle\":\"Converta problemas reais em sucessos de micro SaaS através de ideias validadas, modelos prontos e consultoria especializada.\",\"feature_title_1\":\"Ideias validadas\",\"feature_description_1\":\"Exploração de um banco abrangente de milhares de ideias analisadas para rápida validação e adaptação ao mercado.\",\"feature_title_2\":\"Modelos de negócio com I.A\",\"feature_description_2\":\"Utilização de inteligência artificial para criar planos de negócios otimizados, economizando tempo e recursos.\",\"feature_title_3\":\"Consultoria personalizada\",\"feature_description_3\":\"Apoio sob medida em cada etapa do desenvolvimento, garantindo a eficácia e o sucesso do seu projeto SaaS.\",\"feature_title_4\":\"Ferramentas integradas\",\"feature_description_4\":\"Criação de páginas personalizáveis com integração rápida para marketing e lançamento.\"},\"IdeaCardComponent\":{\"differentials\":\"Diferenciais\",\"features\":\"Funcionalidades\",\"implementation\":\"Implementação\",\"viability\":\"Viabilidade\"},\"FeaturesComponent\":{\"all_in_one\":\"Solução completa e validada\",\"features_title_part1\":\"Acelere sua startup com\",\"features_title_part2\":\"Ideias validadas!\",\"features_subtitle\":\"Economize tempo na pesquisa de mercado e comece a construir seu SaaS com as melhores ideias do mercado.\",\"feature_title_1\":\"Banco de dados de problemas reais\",\"feature_description_1\":\"Explore ideias de negócios baseadas em problemas genuínos discutidos por comunidades online ativas. Foque no que importa: construir um produto de sucesso.\",\"feature_title_2\":\"Banco de Dados de Ideias de Negócios\",\"feature_description_2\":\"Descubra oportunidades inexploradas com soluções geradas por IA, identificando lacunas de mercado e tendências emergentes. Encontre a ideia perfeita para seu próximo Micro SaaS.\",\"feature_title_3\":\"Atualizações constantes\",\"feature_description_3\":\"Receba novas ideias semanalmente e mantenha-se à frente da concorrência. Nosso banco de dados está sempre atualizado com as últimas tendências.\"},\"PriceSection\":{\"title_part_1\":\"Pare de perder tempo pesquisando.\",\"title_part_2\":\"Acesse ideias validadas e construa rápido.\",\"card_tile_1\":\"Básico - Acesso Anual\",\"card_full_price\":\"R$360,00\",\"card_discount_price\":\"R$260,00\",\"card_description\":\"Pagamento único. Crie negócios ilimitados.\",\"card_feature_1\":\"Atualizações semanais\",\"card_feature_2\":\"Consultas ilimitadas\",\"card_feature_3\":\"IdeaForge DB com +3000 ideias\",\"card_feature_4\":\"Pesquisa avançada com filtros\",\"card_feature_5\":\"Sugestões de funcionalidades com IA\",\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"faqSection\":{\"title\":\"Perguntas Frequentes\",\"sub-title\":\"Tem mais dúvidas? Entre em contato por e-mail ou WhatsApp\",\"q1\":\"O que o IdeaForge DB oferece?\",\"r1\":\"O IdeaForge DB oferece acesso a um banco de dados com milhares de ideias de negócios baseadas em problemas reais discutidos por usuários de redes sociais. Você poderá filtrar as ideias por nicho, data de criação e popularidade para encontrar oportunidades validadas e economizar tempo no desenvolvimento de sua startup.\",\"q2\":\"O IdeaForge DB já está disponível?\",\"r2\":\"Estamos finalizando os detalhes do IdeaForge! Cadastre-se agora para ser um dos primeiros a acessar no lançamento e aproveite descontos exclusivos.\",\"q3\":\"Posso obter um reembolso?\",\"r3\":\"O IdeaForge DB é um produto não reembolsável. Por favor, revise os recursos e benefícios antes de adquirir. Se tiver dúvidas, entre em contato conosco.\",\"q4\":\"Com que frequência o IdeaForge DB é atualizado?\",\"r4\":\"Nosso banco de dados é atualizado semanalmente com novas ideias e tendências. Você terá acesso constante a oportunidades frescas.\",\"q5\":\"Que tipo de conteúdo está no IdeaForge DB?\",\"r5\":\"Nosso banco de dados contém ideias de negócios baseadas em problemas reais discutidos por usuários em redes sociais. Além disso, oferecemos sugestões de funcionalidades geradas por IA para ajudar você a criar soluções completas.\",\"q6\":\"Como acesso o IdeaForge DB após a compra?\",\"r6\":\"Após a compra, você receberá um e-mail com os detalhes de acesso à plataforma. Faça login para explorar o banco de dados e começar a construir sua startup.\"},\"bottomSection\":\"$Y\",\"FooterSection\":\"$Y\",\"WaitlistBenefitsSection\":\"$Y\",\"EmailCaptureForm\":\"$Y\"},\"children\":\"$Y\"}}\n"])</script><script>self.__next_f.push([1,"1f:D\"$20\"\n9:[\"$\",\"html\",null,{\"lang\":\"pt\",\"className\":\"scroll-smooth\",\"children\":[[\"$\",\"head\",null,{\"children\":[\"$\",\"link\",null,{\"rel\":\"icon\",\"href\":\"/favicon.ico\"},\"$a\"]},\"$a\"],[\"$\",\"body\",null,{\"children\":\"$L1f\"},\"$a\"]]},\"$a\"]\n"])</script><script>self.__next_f.push([1,"21:I[\"[project]/node_modules/.pnpm/next-intl@3.26.3_next@15.1.4_react-dom@19.0.0_react@19.0.0__react@19.0.0__react@19.0.0/node_modules/next-intl/dist/esm/shared/NextIntlClientProvider.js [app-client] (ecmascript)\",[\"static/chunks/_f7052d._.js\",\"static/chunks/src_app_[locale]_layout_tsx_a54a05._.js\"],\"default\"]\n"])</script><script>self.__next_f.push([1,"1f:[\"$\",\"$L21\",null,{\"locale\":\"pt\",\"now\":\"$D2025-01-12T19:38:09.404Z\",\"timeZone\":\"America/Sao_Paulo\",\"messages\":{\"HeaderComponent\":{\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"HeroComponent\":{\"hero_title_part1\":\"Transforme problemas reais\",\"hero_title_part2\":\"em\",\"hero_title_part3\":\"micro SaaS de sucesso!\",\"hero_subtitle_part1\":\"Para empreendedores e visionários do SaaS: Aceite o desafio e construa seu caminho no mundo SaaS com ferramentas prontas, ideias validadas, e suporte especializado.\",\"hero_subtitle_part2\":\"\",\"hero_discount\":\"R$100 de desconto\",\"hero_remaining\":\"48 vagas restantes\",\"hero_ideias_title_part1\":\"Acesse mais de 3000 ideias\",\"hero_ideias_title_part2\":\"validadas e prontas para ação\",\"call_to_action\":\"Inicie sua Jornada SaaS\",\"ideas\":\"pt\"},\"ValuePropositionComponent\":{\"all_in_one\":\"Solução completa e validada\",\"features_title_part1\":\"Acelere sua startup\",\"features_subtitle\":\"Converta problemas reais em sucessos de micro SaaS através de ideias validadas, modelos prontos e consultoria especializada.\",\"feature_title_1\":\"Ideias validadas\",\"feature_description_1\":\"Exploração de um banco abrangente de milhares de ideias analisadas para rápida validação e adaptação ao mercado.\",\"feature_title_2\":\"Modelos de negócio com I.A\",\"feature_description_2\":\"Utilização de inteligência artificial para criar planos de negócios otimizados, economizando tempo e recursos.\",\"feature_title_3\":\"Consultoria personalizada\",\"feature_description_3\":\"Apoio sob medida em cada etapa do desenvolvimento, garantindo a eficácia e o sucesso do seu projeto SaaS.\",\"feature_title_4\":\"Ferramentas integradas\",\"feature_description_4\":\"Criação de páginas personalizáveis com integração rápida para marketing e lançamento.\"},\"IdeaCardComponent\":{\"differentials\":\"Diferenciais\",\"features\":\"Funcionalidades\",\"implementation\":\"Implementação\",\"viability\":\"Viabilidade\"},\"FeaturesComponent\":{\"all_in_one\":\"Solução completa e validada\",\"features_title_part1\":\"Acelere sua startup com\",\"features_title_part2\":\"Ideias validadas!\",\"features_subtitle\":\"Economize tempo na pesquisa de mercado e comece a construir seu SaaS com as melhores ideias do mercado.\",\"feature_title_1\":\"Banco de dados de problemas reais\",\"feature_description_1\":\"Explore ideias de negócios baseadas em problemas genuínos discutidos por comunidades online ativas. Foque no que importa: construir um produto de sucesso.\",\"feature_title_2\":\"Banco de Dados de Ideias de Negócios\",\"feature_description_2\":\"Descubra oportunidades inexploradas com soluções geradas por IA, identificando lacunas de mercado e tendências emergentes. Encontre a ideia perfeita para seu próximo Micro SaaS.\",\"feature_title_3\":\"Atualizações constantes\",\"feature_description_3\":\"Receba novas ideias semanalmente e mantenha-se à frente da concorrência. Nosso banco de dados está sempre atualizado com as últimas tendências.\"},\"PriceSection\":{\"title_part_1\":\"Pare de perder tempo pesquisando.\",\"title_part_2\":\"Acesse ideias validadas e construa rápido.\",\"card_tile_1\":\"Básico - Acesso Anual\",\"card_full_price\":\"R$360,00\",\"card_discount_price\":\"R$260,00\",\"card_description\":\"Pagamento único. Crie negócios ilimitados.\",\"card_feature_1\":\"Atualizações semanais\",\"card_feature_2\":\"Consultas ilimitadas\",\"card_feature_3\":\"IdeaForge DB com +3000 ideias\",\"card_feature_4\":\"Pesquisa avançada com filtros\",\"card_feature_5\":\"Sugestões de funcionalidades com IA\",\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"faqSection\":{\"title\":\"Perguntas Frequentes\",\"sub-title\":\"Tem mais dúvidas? Entre em contato por e-mail ou WhatsApp\",\"q1\":\"O que o IdeaForge DB oferece?\",\"r1\":\"O IdeaForge DB oferece acesso a um banco de dados com milhares de ideias de negócios baseadas em problemas reais discutidos por usuários de redes sociais. Você poderá filtrar as ideias por nicho, data de criação e popularidade para encontrar oportunidades validadas e economizar tempo no desenvolvimento de sua startup.\",\"q2\":\"O IdeaForge DB já está disponível?\",\"r2\":\"Estamos finalizando os detalhes do IdeaForge! Cadastre-se agora para ser um dos primeiros a acessar no lançamento e aproveite descontos exclusivos.\",\"q3\":\"Posso obter um reembolso?\",\"r3\":\"O IdeaForge DB é um produto não reembolsável. Por favor, revise os recursos e benefícios antes de adquirir. Se tiver dúvidas, entre em contato conosco.\",\"q4\":\"Com que frequência o IdeaForge DB é atualizado?\",\"r4\":\"Nosso banco de dados é atualizado semanalmente com novas ideias e tendências. Você terá acesso constante a oportunidades frescas.\",\"q5\":\"Que tipo de conteúdo está no IdeaForge DB?\",\"r5\":\"Nosso banco de dados contém ideias de negócios baseadas em problemas reais discutidos por usuários em redes sociais. Além disso, oferecemos sugestões de funcionalidades geradas por IA para ajudar você a criar soluções completas.\",\"q6\":\"Como acesso o IdeaForge DB após a compra?\",\"r6\":\"Após a compra, você receberá um e-mail com os detalhes de acesso à plataforma. Faça login para explorar o banco de dados e começar a construir sua startup.\"},\"bottomSection\":{\"title\":\"Receba Ideias Novas Toda Semana!\",\"sub-title\":\"Assine nossa newsletter e descubra semanalmente ideias inovadoras, insights de mercado e dicas exclusivas diretamente no seu e-mail.\",\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"FooterSection\":{\"text1\":\"Desperte sua criatividade.\",\"text2\":\"© 2024 IdeaForge. Todos os direitos reservados.\",\"text3\":\"IdeaForge Construído por BeMySaaS\"},\"WaitlistBenefitsSection\":{\"title\":\"Por que se inscrever na lista de espera?\",\"b1\":\"Acesso antecipado ao nosso banco de dados de 3.000+ ideias de negócios.\",\"b2\":\"Um desconto especial quando lançarmos.\",\"b3\":\"Seja o primeiro a explorar ideias de negócios validadas e tendências.\",\"b4\":\"Receba atualizações sobre o desenvolvimento do produto e suas características.\",\"call_to_action\":\"Inicie sua Jornada SaaS\"},\"EmailCaptureForm\":{\"title\":\"Junte-se à lista de espera\",\"alert\":\"Nome e Email são obrigatórios.\",\"name\":\"Nome\",\"email\":\"Email\",\"phone\":\"Celular (Opcional)\",\"btn\":\"Enviar\",\"msg\":\"Enviado com sucesso\"}},\"children\":[\"$\",\"$L4\",null,{\"parallelRouterKey\":\"children\",\"segmentPath\":[\"children\",\"$0:f:0:1:2:children:0\",\"children\"],\"error\":\"$undefined\",\"errorStyles\":\"$undefined\",\"errorScripts\":\"$undefined\",\"template\":[\"$\",\"$L5\",null,{},null],\"templateStyles\":\"$undefined\",\"templateScripts\":\"$undefined\",\"notFound\":\"$undefined\",\"forbidden\":\"$undefined\",\"unauthorized\":\"$undefined\"},null]},\"$20\"]\n"])</script><nextjs-portal><template shadowrootmode="open"><style>
        :host {
          all: initial;

          /* the direction property is not reset by 'all' */
          direction: ltr;
        }

        /*!
         * Bootstrap Reboot v4.4.1 (https://getbootstrap.com/)
         * Copyright 2011-2019 The Bootstrap Authors
         * Copyright 2011-2019 Twitter, Inc.
         * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
         * Forked from Normalize.css, licensed MIT (https://github.com/necolas/normalize.css/blob/master/LICENSE.md)
         */
        *,
        *::before,
        *::after {
          box-sizing: border-box;
        }

        :host {
          font-family: sans-serif;
          line-height: 1.15;
          -webkit-text-size-adjust: 100%;
          -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
        }

        article,
        aside,
        figcaption,
        figure,
        footer,
        header,
        hgroup,
        main,
        nav,
        section {
          display: block;
        }

        :host {
          margin: 0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
            'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
            'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
            'Noto Color Emoji';
          font-size: 16px;
          font-weight: 400;
          line-height: 1.5;
          color: var(--color-font);
          text-align: left;
          background-color: #fff;
        }

        [tabindex='-1']:focus:not(:focus-visible) {
          outline: 0 !important;
        }

        hr {
          box-sizing: content-box;
          height: 0;
          overflow: visible;
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
          margin-top: 0;
          margin-bottom: 8px;
        }

        p {
          margin-top: 0;
          margin-bottom: 16px;
        }

        abbr[title],
        abbr[data-original-title] {
          text-decoration: underline;
          -webkit-text-decoration: underline dotted;
          text-decoration: underline dotted;
          cursor: help;
          border-bottom: 0;
          -webkit-text-decoration-skip-ink: none;
          text-decoration-skip-ink: none;
        }

        address {
          margin-bottom: 16px;
          font-style: normal;
          line-height: inherit;
        }

        ol,
        ul,
        dl {
          margin-top: 0;
          margin-bottom: 16px;
        }

        ol ol,
        ul ul,
        ol ul,
        ul ol {
          margin-bottom: 0;
        }

        dt {
          font-weight: 700;
        }

        dd {
          margin-bottom: 8px;
          margin-left: 0;
        }

        blockquote {
          margin: 0 0 16px;
        }

        b,
        strong {
          font-weight: bolder;
        }

        small {
          font-size: 80%;
        }

        sub,
        sup {
          position: relative;
          font-size: 75%;
          line-height: 0;
          vertical-align: baseline;
        }

        sub {
          bottom: -0.25em;
        }

        sup {
          top: -0.5em;
        }

        a {
          color: #007bff;
          text-decoration: none;
          background-color: transparent;
        }

        a:hover {
          color: #0056b3;
          text-decoration: underline;
        }

        a:not([href]) {
          color: inherit;
          text-decoration: none;
        }

        a:not([href]):hover {
          color: inherit;
          text-decoration: none;
        }

        pre,
        code,
        kbd,
        samp {
          font-family: SFMono-Regular, Menlo, Monaco, Consolas,
            'Liberation Mono', 'Courier New', monospace;
          font-size: 1em;
        }

        pre {
          margin-top: 0;
          margin-bottom: 16px;
          overflow: auto;
        }

        figure {
          margin: 0 0 16px;
        }

        img {
          vertical-align: middle;
          border-style: none;
        }

        svg {
          overflow: hidden;
          vertical-align: middle;
        }

        table {
          border-collapse: collapse;
        }

        caption {
          padding-top: 12px;
          padding-bottom: 12px;
          color: #6c757d;
          text-align: left;
          caption-side: bottom;
        }

        th {
          text-align: inherit;
        }

        label {
          display: inline-block;
          margin-bottom: 8px;
        }

        button {
          border-radius: 0;
        }

        button:focus {
          outline: 1px dotted;
          outline: 5px auto -webkit-focus-ring-color;
        }

        input,
        button,
        select,
        optgroup,
        textarea {
          margin: 0;
          font-family: inherit;
          font-size: inherit;
          line-height: inherit;
        }

        button,
        input {
          overflow: visible;
        }

        button,
        select {
          text-transform: none;
        }

        select {
          word-wrap: normal;
        }

        button,
        [type='button'],
        [type='reset'],
        [type='submit'] {
          -webkit-appearance: button;
        }

        button:not(:disabled),
        [type='button']:not(:disabled),
        [type='reset']:not(:disabled),
        [type='submit']:not(:disabled) {
          cursor: pointer;
        }

        button::-moz-focus-inner,
        [type='button']::-moz-focus-inner,
        [type='reset']::-moz-focus-inner,
        [type='submit']::-moz-focus-inner {
          padding: 0;
          border-style: none;
        }

        input[type='radio'],
        input[type='checkbox'] {
          box-sizing: border-box;
          padding: 0;
        }

        input[type='date'],
        input[type='time'],
        input[type='datetime-local'],
        input[type='month'] {
          -webkit-appearance: listbox;
        }

        textarea {
          overflow: auto;
          resize: vertical;
        }

        fieldset {
          min-width: 0;
          padding: 0;
          margin: 0;
          border: 0;
        }

        legend {
          display: block;
          width: 100%;
          max-width: 100%;
          padding: 0;
          margin-bottom: 8px;
          font-size: 24px;
          line-height: inherit;
          color: inherit;
          white-space: normal;
        }

        progress {
          vertical-align: baseline;
        }

        [type='number']::-webkit-inner-spin-button,
        [type='number']::-webkit-outer-spin-button {
          height: auto;
        }

        [type='search'] {
          outline-offset: -2px;
          -webkit-appearance: none;
        }

        [type='search']::-webkit-search-decoration {
          -webkit-appearance: none;
        }

        ::-webkit-file-upload-button {
          font: inherit;
          -webkit-appearance: button;
        }

        output {
          display: inline-block;
        }

        summary {
          display: list-item;
          cursor: pointer;
        }

        template {
          display: none;
        }

        [hidden] {
          display: none !important;
        }
      </style><style>
        :host {
          --size-gap-half: 4px;
          --size-gap: 8px;
          --size-gap-double: 16px;
          --size-gap-triple: 24px;
          --size-gap-quad: 32px;

          --size-font-small: 14px;
          --size-font: 16px;
          --size-font-big: 20px;
          --size-font-bigger: 24px;

          --color-background: white;
          --color-font: #757575;
          --color-backdrop: rgba(17, 17, 17, 0.2);
          --color-border-shadow: rgba(0, 0, 0, 0.145);

          --color-title-color: #1f1f1f;
          --color-stack-h6: #222;
          --color-stack-headline: #666;
          --color-stack-subline: #999;
          --color-stack-notes: #777;

          --color-accents-1: #808080;
          --color-accents-2: #222222;
          --color-accents-3: #404040;

          --color-text-color-red-1: #ff5555;
          --color-text-background-red-1: #fff9f9;

          --font-stack-monospace: 'SFMono-Regular', Consolas, 'Liberation Mono',
            Menlo, Courier, monospace;
          --font-stack-sans: -apple-system, 'Source Sans Pro', sans-serif;

          --color-ansi-selection: rgba(95, 126, 151, 0.48);
          --color-ansi-bg: #111111;
          --color-ansi-fg: #cccccc;

          --color-ansi-white: #777777;
          --color-ansi-black: #141414;
          --color-ansi-blue: #00aaff;
          --color-ansi-cyan: #88ddff;
          --color-ansi-green: #98ec65;
          --color-ansi-magenta: #aa88ff;
          --color-ansi-red: #ff5555;
          --color-ansi-yellow: #ffcc33;
          --color-ansi-bright-white: #ffffff;
          --color-ansi-bright-black: #777777;
          --color-ansi-bright-blue: #33bbff;
          --color-ansi-bright-cyan: #bbecff;
          --color-ansi-bright-green: #b6f292;
          --color-ansi-bright-magenta: #cebbff;
          --color-ansi-bright-red: #ff8888;
          --color-ansi-bright-yellow: #ffd966;
        }

        @media (prefers-color-scheme: dark) {
          :host {
            --color-background: rgb(28, 28, 30);
            --color-font: white;
            --color-backdrop: rgb(44, 44, 46);
            --color-border-shadow: rgba(255, 255, 255, 0.145);

            --color-title-color: #fafafa;
            --color-stack-h6: rgb(200, 200, 204);
            --color-stack-headline: rgb(99, 99, 102);
            --color-stack-notes: #a9a9a9;
            --color-stack-subline: rgb(121, 121, 121);

            --color-accents-3: rgb(118, 118, 118);

            --color-text-background-red-1: #2a1e1e;
          }
        }

        .mono {
          font-family: var(--font-stack-monospace);
        }

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
          margin-bottom: var(--size-gap);
          font-weight: 500;
          line-height: 1.5;
        }
      </style><style>
        
  [data-nextjs-dialog-overlay] {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    overflow: auto;
    z-index: 9000;

    display: flex;
    align-content: center;
    align-items: center;
    flex-direction: column;
    padding: 10vh 15px 0;
  }

  @media (max-height: 812px) {
    [data-nextjs-dialog-overlay] {
      padding: 15px 15px 0;
    }
  }

  [data-nextjs-dialog-backdrop] {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background-color: var(--color-backdrop);
    pointer-events: all;
    z-index: -1;
  }

  [data-nextjs-dialog-backdrop-fixed] {
    cursor: not-allowed;
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
  }

        
  .nextjs-toast {
    position: fixed;
    bottom: var(--size-gap-double);
    left: var(--size-gap-double);
    max-width: 420px;
    z-index: 9000;
    box-shadow: 0px var(--size-gap-double) var(--size-gap-quad)
      rgba(0, 0, 0, 0.25);
  }

  @media (max-width: 440px) {
    .nextjs-toast {
      max-width: 90vw;
      left: 5vw;
    }
  }

  .nextjs-toast-errors-parent {
    padding: 16px;
    border-radius: var(--size-gap-quad);
    font-weight: 500;
    color: var(--color-ansi-bright-white);
    background-color: var(--color-ansi-red);
  }

  .nextjs-static-indicator-toast-wrapper {
    width: 30px;
    height: 30px;
    overflow: hidden;
    border: 0;
    border-radius: var(--size-gap-triple);
    background: var(--color-background);
    color: var(--color-font);
    transition: all 0.3s ease-in-out;
    box-shadow:
      inset 0 0 0 1px var(--color-border-shadow),
      0 11px 40px 0 rgba(0, 0, 0, 0.25),
      0 2px 10px 0 rgba(0, 0, 0, 0.12);
  }

  .nextjs-static-indicator-toast-wrapper:hover {
    width: 140px;
  }

  .nextjs-static-indicator-toast-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
  }

  .nextjs-static-indicator-toast-text {
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    white-space: nowrap;
    transition: opacity 0.3s ease-in-out;
    line-height: 30px;
    position: absolute;
    left: 30px;
    top: 0;
  }

  .nextjs-static-indicator-toast-wrapper:hover
    .nextjs-static-indicator-toast-text {
    opacity: 1;
  }

  .nextjs-static-indicator-toast-wrapper button {
    color: var(--color-font);
    opacity: 0.8;
    background: none;
    border: none;
    margin-left: 6px;
    margin-top: -2px;
    outline: 0;
  }

  .nextjs-static-indicator-toast-wrapper button:focus {
    opacity: 1;
  }

  .nextjs-static-indicator-toast-wrapper button > svg {
    width: 16px;
    height: 16px;
  }

        
  [data-nextjs-dialog] {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-right: auto;
    margin-left: auto;
    outline: none;
    background: var(--color-background);
    border-radius: var(--size-gap);
    box-shadow: 0 var(--size-gap-half) var(--size-gap-double)
      rgba(0, 0, 0, 0.25);
    max-height: calc(100% - 56px);
    overflow-y: hidden;
  }

  @media (max-height: 812px) {
    [data-nextjs-dialog-overlay] {
      max-height: calc(100% - 15px);
    }
  }

  @media (min-width: 576px) {
    [data-nextjs-dialog] {
      max-width: 540px;
      box-shadow: 0 var(--size-gap) var(--size-gap-quad) rgba(0, 0, 0, 0.25);
    }
  }

  @media (min-width: 768px) {
    [data-nextjs-dialog] {
      max-width: 720px;
    }
  }

  @media (min-width: 992px) {
    [data-nextjs-dialog] {
      max-width: 960px;
    }
  }

  [data-nextjs-dialog-banner] {
    position: relative;
  }
  [data-nextjs-dialog-banner].banner-warning {
    border-color: var(--color-ansi-yellow);
  }
  [data-nextjs-dialog-banner].banner-error {
    border-color: var(--color-ansi-red);
  }

  [data-nextjs-dialog-banner]::after {
    z-index: 2;
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
    /* banner width: */
    border-top-width: var(--size-gap-half);
    border-bottom-width: 0;
    border-top-style: solid;
    border-bottom-style: solid;
    border-top-color: inherit;
    border-bottom-color: transparent;
  }

  [data-nextjs-dialog-content] {
    overflow-y: auto;
    border: none;
    margin: 0;
    /* calc(padding + banner width offset) */
    padding: calc(var(--size-gap-double) + var(--size-gap-half))
      var(--size-gap-double);
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  [data-nextjs-dialog-content] > [data-nextjs-dialog-header] {
    flex-shrink: 0;
    margin-bottom: var(--size-gap-double);
  }
  [data-nextjs-dialog-content] > [data-nextjs-dialog-body] {
    position: relative;
    flex: 1 1 auto;
  }

        
  [data-nextjs-dialog-left-right] {
    display: flex;
    flex-direction: row;
    align-content: center;
    align-items: center;
    justify-content: space-between;
  }
  [data-nextjs-dialog-left-right] > nav {
    flex: 1;
    display: flex;
    align-items: center;
    margin-right: var(--size-gap);
  }
  [data-nextjs-dialog-left-right] > nav > button {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    width: calc(var(--size-gap-double) + var(--size-gap));
    height: calc(var(--size-gap-double) + var(--size-gap));
    font-size: 0;
    border: none;
    background-color: rgba(255, 85, 85, 0.1);
    color: var(--color-ansi-red);
    cursor: pointer;
    transition: background-color 0.25s ease;
  }
  [data-nextjs-dialog-left-right] > nav > button > svg {
    width: auto;
    height: calc(var(--size-gap) + var(--size-gap-half));
  }
  [data-nextjs-dialog-left-right] > nav > button:hover {
    background-color: rgba(255, 85, 85, 0.2);
  }
  [data-nextjs-dialog-left-right] > nav > button:disabled {
    background-color: rgba(255, 85, 85, 0.1);
    color: rgba(255, 85, 85, 0.4);
    cursor: not-allowed;
  }

  [data-nextjs-dialog-left-right] > nav > button:first-of-type {
    border-radius: var(--size-gap-half) 0 0 var(--size-gap-half);
    margin-right: 1px;
  }
  [data-nextjs-dialog-left-right] > nav > button:last-of-type {
    border-radius: 0 var(--size-gap-half) var(--size-gap-half) 0;
  }

  [data-nextjs-dialog-left-right] > button:last-of-type {
    border: 0;
    padding: 0;

    background-color: transparent;
    appearance: none;

    opacity: 0.4;
    transition: opacity 0.25s ease;

    color: var(--color-font);
  }
  [data-nextjs-dialog-left-right] > button:last-of-type:hover {
    opacity: 0.7;
  }

        
  [data-nextjs-codeframe] {
    overflow: auto;
    border-radius: var(--size-gap-half);
    background-color: var(--color-ansi-bg);
    color: var(--color-ansi-fg);
    margin-bottom: var(--size-gap-double);
  }
  [data-nextjs-codeframe]::selection,
  [data-nextjs-codeframe] *::selection {
    background-color: var(--color-ansi-selection);
  }
  [data-nextjs-codeframe] * {
    color: inherit;
    background-color: transparent;
    font-family: var(--font-stack-monospace);
  }

  [data-nextjs-codeframe] > * {
    margin: 0;
    padding: calc(var(--size-gap) + var(--size-gap-half))
      calc(var(--size-gap-double) + var(--size-gap-half));
  }
  [data-nextjs-codeframe] > div {
    display: inline-block;
    width: auto;
    min-width: 100%;
    border-bottom: 1px solid var(--color-ansi-bright-black);
  }
  [data-nextjs-codeframe] > div > p {
    display: flex;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
    margin: 0;
  }
  [data-nextjs-codeframe] > div > p:hover {
    text-decoration: underline dotted;
  }
  [data-nextjs-codeframe] div > p > svg {
    width: auto;
    height: 1em;
    margin-left: 8px;
  }
  [data-nextjs-codeframe] div > pre {
    overflow: hidden;
    display: inline-block;
  }

        
  [data-nextjs-terminal] {
    border-radius: var(--size-gap-half);
    background-color: var(--color-ansi-bg);
    color: var(--color-ansi-fg);
  }
  [data-nextjs-terminal]::selection,
  [data-nextjs-terminal] *::selection {
    background-color: var(--color-ansi-selection);
  }
  [data-nextjs-terminal] * {
    color: inherit;
    background-color: transparent;
    font-family: var(--font-stack-monospace);
  }
  [data-nextjs-terminal] > * {
    margin: 0;
    padding: calc(var(--size-gap) + var(--size-gap-half))
      calc(var(--size-gap-double) + var(--size-gap-half));
  }

  [data-nextjs-terminal] pre {
    white-space: pre-wrap;
    word-break: break-word;
  }

  [data-with-open-in-editor-link] svg {
    width: auto;
    height: var(--size-font-small);
    margin-left: var(--size-gap);
  }
  [data-with-open-in-editor-link] {
    cursor: pointer;
  }
  [data-with-open-in-editor-link]:hover {
    text-decoration: underline dotted;
  }
  [data-with-open-in-editor-link-source-file] {
    border-bottom: 1px solid var(--color-ansi-bright-black);
    display: flex;
    align-items: center;
    justify-content: space-between;
    line-break: anywhere;
  }
  [data-with-open-in-editor-link-import-trace] {
    margin-left: var(--size-gap-double);
  }
  [data-nextjs-terminal] a {
    color: inherit;
  }

        
  h1.nextjs__container_errors_label {
    font-size: var(--size-font-big);
    line-height: var(--size-font-bigger);
    font-weight: bold;
    margin: var(--size-gap-double) 0;
  }
  .nextjs-container-errors-header p {
    font-size: var(--size-font-small);
    line-height: var(--size-font-big);
    white-space: pre-wrap;
  }
  .nextjs-container-errors-body footer {
    margin-top: var(--size-gap);
  }
  .nextjs-container-errors-body footer p {
    margin: 0;
  }

  .nextjs-container-errors-body small {
    color: var(--color-font);
  }

        
  .nextjs-error-with-static {
    bottom: calc(var(--size-gap-double) * 4.5);
  }
  .nextjs-container-errors-header {
    position: relative;
  }
  .nextjs-container-errors-header > h1 {
    font-size: var(--size-font-big);
    line-height: var(--size-font-bigger);
    font-weight: bold;
    margin: calc(var(--size-gap-double) * 1.5) 0;
    color: var(--color-title-h1);
  }
  .nextjs-container-errors-header small {
    font-size: var(--size-font-small);
    color: var(--color-accents-1);
    margin-left: var(--size-gap-double);
  }
  .nextjs-container-errors-header small > span {
    font-family: var(--font-stack-monospace);
  }
  .nextjs-container-errors-header p {
    font-size: var(--size-font-small);
    line-height: var(--size-font-big);
    white-space: pre-wrap;
  }
  .nextjs__container_errors_desc {
    font-family: var(--font-stack-monospace);
    padding: var(--size-gap) var(--size-gap-double);
    border-left: 2px solid var(--color-text-color-red-1);
    margin-top: var(--size-gap);
    font-weight: bold;
    color: var(--color-text-color-red-1);
    background-color: var(--color-text-background-red-1);
  }
  p.nextjs__container_errors__link {
    margin: var(--size-gap-double) auto;
    color: var(--color-text-color-red-1);
    font-weight: 600;
    font-size: 15px;
  }
  p.nextjs__container_errors__notes {
    margin: var(--size-gap-double) auto;
    color: var(--color-stack-notes);
    font-weight: 600;
    font-size: 15px;
  }
  .nextjs-container-errors-header > div > small {
    margin: 0;
    margin-top: var(--size-gap-half);
  }
  .nextjs-container-errors-header > p > a {
    color: inherit;
    font-weight: bold;
  }
  .nextjs-container-errors-body > h2:not(:first-child) {
    margin-top: calc(var(--size-gap-double) + var(--size-gap));
  }
  .nextjs-container-errors-body > h2 {
    color: var(--color-title-color);
    margin-bottom: var(--size-gap);
    font-size: var(--size-font-big);
  }
  .nextjs__container_errors__component-stack {
    padding: 12px 32px;
    color: var(--color-ansi-fg);
    background: var(--color-ansi-bg);
  }
  .nextjs-toast-errors-parent {
    cursor: pointer;
    transition: transform 0.2s ease;
  }
  .nextjs-toast-errors-parent:hover {
    transform: scale(1.1);
  }
  .nextjs-toast-errors {
    display: flex;
    align-items: center;
    justify-content: flex-start;
  }
  .nextjs-toast-errors > svg {
    margin-right: var(--size-gap);
  }
  .nextjs-toast-hide-button {
    margin-left: var(--size-gap-triple);
    border: none;
    background: none;
    color: var(--color-ansi-bright-white);
    padding: 0;
    transition: opacity 0.25s ease;
    opacity: 0.7;
  }
  .nextjs-toast-hide-button:hover {
    opacity: 1;
  }
  .nextjs-container-errors-header
    > .nextjs-container-build-error-version-status {
    position: absolute;
    top: 0;
    right: 0;
  }
  .nextjs__container_errors_inspect_copy_button {
    cursor: pointer;
    background: none;
    border: none;
    color: var(--color-ansi-bright-white);
    font-size: 1.5rem;
    padding: 0;
    margin: 0;
    margin-left: var(--size-gap);
    transition: opacity 0.25s ease;
  }
  .nextjs__container_errors__error_title {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .nextjs-data-runtime-error-inspect-link,
  .nextjs-data-runtime-error-inspect-link:hover {
    margin: 0 8px;
    color: inherit;
  }

        
  [data-nextjs-call-stack-frame]:not(:last-child),
  [data-nextjs-component-stack-frame]:not(:last-child) {
    margin-bottom: var(--size-gap-double);
  }

  [data-expand-ignore-button]:focus:not(:focus-visible),
  [data-expand-ignore-button] {
    background: none;
    border: none;
    color: var(--color-font);
    cursor: pointer;
    font-size: var(--size-font);
    margin: var(--size-gap) 0;
    padding: 0;
    text-decoration: underline;
    outline: none;
  }

  [data-nextjs-data-runtime-error-copy-button],
  [data-nextjs-data-runtime-error-copy-button]:focus:not(:focus-visible) {
    position: relative;
    margin-left: var(--size-gap);
    padding: 0;
    border: none;
    background: none;
    outline: none;
  }
  [data-nextjs-data-runtime-error-copy-button] > svg {
    vertical-align: middle;
  }
  .nextjs-data-runtime-error-copy-button {
    color: inherit;
  }
  .nextjs-data-runtime-error-copy-button--initial:hover {
    cursor: pointer;
  }
  .nextjs-data-runtime-error-copy-button[aria-disabled='true'] {
    opacity: 0.3;
    cursor: not-allowed;
  }
  .nextjs-data-runtime-error-copy-button--error,
  .nextjs-data-runtime-error-copy-button--error:hover {
    color: var(--color-ansi-red);
  }
  .nextjs-data-runtime-error-copy-button--success {
    color: var(--color-ansi-green);
  }

  [data-nextjs-call-stack-frame] > h3,
  [data-nextjs-component-stack-frame] > h3 {
    margin-top: 0;
    margin-bottom: 0;
    font-family: var(--font-stack-monospace);
    font-size: var(--size-font);
  }
  [data-nextjs-call-stack-frame] > h3[data-nextjs-frame-expanded='false'] {
    color: #666;
    display: inline-block;
  }
  [data-nextjs-call-stack-frame] > div,
  [data-nextjs-component-stack-frame] > div {
    display: flex;
    align-items: center;
    padding-left: calc(var(--size-gap) + var(--size-gap-half));
    font-size: var(--size-font-small);
    color: #999;
  }
  [data-nextjs-call-stack-frame] > div > svg,
  [data-nextjs-component-stack-frame] > [role='link'] > svg {
    width: auto;
    height: var(--size-font-small);
    margin-left: var(--size-gap);
    flex-shrink: 0;
    display: none;
  }

  [data-nextjs-call-stack-frame] > div[data-has-source],
  [data-nextjs-component-stack-frame] > [role='link'] {
    cursor: pointer;
  }
  [data-nextjs-call-stack-frame] > div[data-has-source]:hover,
  [data-nextjs-component-stack-frame] > [role='link']:hover {
    text-decoration: underline dotted;
  }
  [data-nextjs-call-stack-frame] > div[data-has-source] > svg,
  [data-nextjs-component-stack-frame] > [role='link'] > svg {
    display: unset;
  }

  [data-nextjs-call-stack-framework-icon] {
    margin-right: var(--size-gap);
  }
  [data-nextjs-call-stack-framework-icon='next'] > mask {
    mask-type: alpha;
  }
  [data-nextjs-call-stack-framework-icon='react'] {
    color: rgb(20, 158, 202);
  }
  [data-nextjs-collapsed-call-stack-details][open]
    [data-nextjs-call-stack-chevron-icon] {
    transform: rotate(90deg);
  }
  [data-nextjs-collapsed-call-stack-details] summary {
    display: flex;
    align-items: center;
    margin-bottom: var(--size-gap);
    list-style: none;
  }
  [data-nextjs-collapsed-call-stack-details] summary::-webkit-details-marker {
    display: none;
  }

  [data-nextjs-collapsed-call-stack-details] h3 {
    color: #666;
  }
  [data-nextjs-collapsed-call-stack-details] [data-nextjs-call-stack-frame] {
    margin-bottom: var(--size-gap-double);
  }

  [data-nextjs-container-errors-pseudo-html] {
    position: relative;
  }
  [data-nextjs-container-errors-pseudo-html-collapse] {
    position: absolute;
    left: 10px;
    top: 10px;
    color: inherit;
    background: none;
    border: none;
    padding: 0;
  }
  [data-nextjs-container-errors-pseudo-html--diff='add'] {
    color: var(--color-ansi-green);
  }
  [data-nextjs-container-errors-pseudo-html--diff='remove'] {
    color: var(--color-ansi-red);
  }
  [data-nextjs-container-errors-pseudo-html--tag-error] {
    color: var(--color-ansi-red);
    font-weight: bold;
  }
  /* hide but text are still accessible in DOM */
  [data-nextjs-container-errors-pseudo-html--hint] {
    display: inline-block;
    font-size: 0;
  }
  [data-nextjs-container-errors-pseudo-html--tag-adjacent='false'] {
    color: var(--color-accents-1);
  }

        
  .nextjs-container-build-error-version-status {
    flex: 1;
    text-align: right;
    font-size: var(--size-font-small);
  }
  .nextjs-container-build-error-version-status span {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 5px;
    background: var(--color-ansi-bright-black);
  }
  .nextjs-container-build-error-version-status span.fresh {
    background: var(--color-ansi-green);
  }
  .nextjs-container-build-error-version-status span.stale {
    background: var(--color-ansi-yellow);
  }
  .nextjs-container-build-error-version-status span.outdated {
    background: var(--color-ansi-red);
  }

      </style></template></nextjs-portal><next-route-announcer style="position: absolute;"><template shadowrootmode="open"><div aria-live="assertive" id="__next-route-announcer__" role="alert" style="position: absolute; border: 0px; height: 1px; margin: -1px; padding: 0px; width: 1px; clip: rect(0px, 0px, 0px, 0px); overflow: hidden; white-space: nowrap; overflow-wrap: normal;"></div></template></next-route-announcer><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/[turbopack]_browser_dev_hmr-client_d6d8d4._.js"></script><script src="./IdeaForge DB_ Como criar Micro SaaS lucrativos resolvendo problemas reais_files/[turbopack]_browser_dev_hmr-client_hmr-client_ts_abec30._.js"></script></body></html>
```

## public/user3.jpg
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

## public/user2.jpg
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

## public/video-demo.mp4
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xd9 in position 35: invalid continuation byte
```

## public/curve-4.png.webp
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x82 in position 4: invalid start byte
```

## public/user1.jpg
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte
```

## public/features-preview.png
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x89 in position 0: invalid start byte
```

## public/ai.svg
```
<?xml version="1.0" encoding="UTF-8"?><svg id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><style>.cls-1{fill:#fff;}.cls-2{fill:#635bff;}</style></defs><path class="cls-2" d="m54.53,57.01l-4.19-11.55c-.29-.79-.92-1.72-2.26-1.72s-1.97.94-2.26,1.73l-4.18,11.54c-.28.73-.28.79-.28,1.11,0,.69.65,1.3,1.39,1.3.51,0,1-.12,1.41-1.59l.48-1.75h6.9l.48,1.75c.42,1.47.87,1.59,1.41,1.59.75,0,1.39-.59,1.39-1.3,0-.3,0-.38-.28-1.1Zm-8.37-3.76l1.95-6.11,1.95,6.11h-3.9Z"/><polygon class="cls-1" points="46.16 53.25 50.05 53.25 48.1 47.14 46.16 53.25"/><path class="cls-2" d="m60.27,43.8c-.48,0-.98.28-1.19.66-.14.31-.18.45-.18,1.31v11.62c0,.89.02.99.19,1.32.2.37.7.65,1.18.65s.95-.28,1.16-.66c.14-.31.18-.45.18-1.31v-11.62c0-.89-.02-.99-.19-1.32-.18-.36-.69-.65-1.15-.65Z"/><path class="cls-2" d="m48.14,69.81h8.06v12.15l-.34.11c-.58.19-1.11.51-1.54.94-.72.72-1.12,1.68-1.12,2.71s.4,1.98,1.13,2.71c1.45,1.45,3.95,1.45,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.12-2.7c-.42-.42-.94-.74-1.5-.93l-.33-.11v-12.15h8.15v9.77c0,1.04.41,2.01,1.14,2.75.74.74,1.71,1.14,2.75,1.14h3.89l.11.34c.18.57.51,1.1.93,1.52,1.44,1.44,3.95,1.45,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.12-2.7c-1.44-1.44-3.95-1.45-5.41,0-.42.42-.74.95-.93,1.51l-.11.33h-3.89c-.58,0-1.14-.23-1.55-.65-.41-.41-.64-.96-.64-1.55v-9.82l.35-.1c.63-.18,1.21-.52,1.67-.99.74-.73,1.14-1.71,1.14-2.74v-4.14h13.31l.11.33c.19.56.51,1.08.93,1.5,1.45,1.44,3.95,1.45,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.12-2.7c-1.44-1.44-3.95-1.45-5.41,0-.43.43-.75.96-.94,1.54l-.11.34h-13.3v-8.06h7.24l.11.33c.19.56.51,1.08.93,1.5,1.44,1.44,3.95,1.45,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.12-2.7c-1.45-1.45-3.97-1.45-5.41,0-.43.43-.76.96-.94,1.54l-.11.34h-7.23v-8.06h13.35l.11.34c.19.58.51,1.11.94,1.54,1.45,1.45,3.96,1.44,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.13-2.71c-1.45-1.45-3.96-1.44-5.41,0-.42.42-.74.94-.93,1.5l-.11.33h-13.36v-4.14c0-1.03-.4-2.01-1.14-2.74-.47-.47-1.04-.81-1.67-.99l-.35-.1v-9.81c0-.58.23-1.13.64-1.55.41-.41.97-.64,1.55-.64h3.89l.11.33c.19.57.51,1.09.94,1.52,1.45,1.45,3.96,1.44,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.13-2.71c-1.45-1.45-3.96-1.44-5.41,0-.43.43-.75.95-.93,1.52l-.11.34h-3.89c-1.04,0-2.01.41-2.75,1.14-.74.74-1.14,1.71-1.14,2.75v9.77h-8.06v-6.07l.34-.11c.58-.18,1.11-.51,1.54-.94.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.13-2.71c-1.45-1.45-3.97-1.44-5.41,0-.72.72-1.12,1.68-1.12,2.71s.4,1.98,1.12,2.71c.42.42.94.74,1.5.93l.33.11v6.09h-8.06v-12.14l.34-.11c.57-.18,1.11-.51,1.54-.94.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.12-2.71c-1.45-1.45-3.95-1.45-5.41,0-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.12,2.7c.42.42.94.74,1.5.93l.33.11v12.16h-8.15v-9.77c0-1.04-.41-2.01-1.14-2.75s-1.71-1.14-2.75-1.14h-3.89l-.11-.34c-.18-.57-.51-1.1-.93-1.52-1.44-1.44-3.96-1.45-5.41,0-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.13,2.71c1.45,1.44,3.95,1.45,5.41,0,.42-.42.74-.95.93-1.51l.11-.33h3.89c.58,0,1.13.23,1.55.64.42.41.64.97.64,1.55v9.84l-.34.11c-.58.19-1.12.52-1.56.95-.74.74-1.14,1.71-1.14,2.74v4.14h-13.36l-.11-.33c-.19-.56-.51-1.08-.93-1.5-1.44-1.44-3.95-1.45-5.41,0-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.12,2.7c1.44,1.44,3.95,1.45,5.41,0,.43-.43.75-.96.94-1.53l.11-.34h13.35v8.06h-7.23l-.11-.34c-.18-.58-.51-1.11-.94-1.54-.72-.72-1.68-1.12-2.7-1.12s-1.98.4-2.71,1.13c-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.13,2.71c1.45,1.45,3.96,1.44,5.41,0,.42-.42.74-.94.93-1.5l.11-.33h7.24v8.06h-13.3l-.11-.34c-.19-.57-.51-1.11-.95-1.54-1.45-1.44-3.96-1.44-5.41,0-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.13,2.71c1.45,1.44,3.95,1.45,5.41,0,.42-.42.74-.94.92-1.5l.11-.33h13.31v4.14c0,1.03.4,2.01,1.14,2.74.44.43.97.76,1.56.95l.34.11v9.84c0,.58-.23,1.13-.64,1.55-.41.41-.97.64-1.55.64h-3.89l-.11-.33c-.19-.57-.51-1.09-.94-1.52-1.45-1.44-3.95-1.45-5.41,0-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.13,2.71c1.45,1.45,3.97,1.44,5.41,0,.43-.43.75-.95.93-1.52l.11-.34h3.89c1.04,0,2.01-.41,2.75-1.14.74-.74,1.14-1.71,1.14-2.75v-9.77h8.06v6.08l-.34.11c-.58.18-1.11.51-1.54.94-.72.72-1.12,1.68-1.12,2.7s.4,1.98,1.13,2.71c1.45,1.44,3.95,1.45,5.41,0,.72-.72,1.12-1.68,1.12-2.7s-.4-1.98-1.13-2.71c-.42-.42-.94-.74-1.5-.92l-.33-.11v-6.09Zm8.89,18.03c-.57,0-1.1-.22-1.51-.62-.4-.4-.62-.94-.62-1.51s.22-1.1.62-1.5c.81-.81,2.22-.79,3.01,0,.4.4.62.94.62,1.5s-.22,1.1-.62,1.51c-.4.4-.94.62-1.51.62Zm20.55-3.09c-.57,0-1.1-.22-1.5-.62s-.62-.94-.62-1.5.22-1.11.62-1.51c.79-.8,2.2-.8,3.01,0,.4.4.62.93.62,1.5s-.22,1.1-.62,1.51c-.4.4-.94.62-1.51.62Zm-50.73,0c-.57,0-1.1-.22-1.51-.62-.4-.4-.62-.94-.62-1.51s.22-1.11.62-1.51c.81-.8,2.21-.8,3.02,0,.39.39.62.93.62,1.48,0,.58-.22,1.12-.62,1.53s-.94.62-1.5.62Zm20.42-2.98c-.57,0-1.1-.22-1.51-.62h0c-.4-.4-.62-.94-.62-1.51s.22-1.1.62-1.5c.81-.81,2.21-.8,3.01,0,.4.4.62.94.62,1.51s-.22,1.1-.62,1.51c-.4.4-.94.62-1.51.62Zm19.76-13.66h-29.5c-.58,0-1.13-.23-1.54-.64-.41-.41-.64-.96-.64-1.54v-29.5c0-.58.23-1.13.64-1.54s.93-.63,1.5-.64h29.41c.48,0,1.11.07,1.67.64.41.41.64.96.64,1.54v29.5c0,.58-.23,1.13-.64,1.54-.41.41-.96.64-1.54.64Zm-50.44-5.07c-.57,0-1.1-.22-1.51-.62-.4-.4-.62-.94-.62-1.51s.22-1.1.62-1.5c.81-.81,2.21-.8,3.01,0,.39.4.61.92.62,1.48v.06c0,.56-.23,1.08-.62,1.47-.4.4-.94.62-1.51.62Zm71.37,0c-.57,0-1.1-.22-1.51-.62-.39-.39-.61-.92-.62-1.48h0c0-.6.21-1.13.62-1.54.81-.8,2.21-.8,3.01,0,.4.4.62.93.62,1.5s-.22,1.11-.62,1.51c-.4.4-.94.62-1.51.62Zm-65.3-9.76c-.57,0-1.1-.22-1.51-.62-.4-.4-.62-.94-.62-1.51s.22-1.1.62-1.51h0c.8-.8,2.2-.8,3.01,0,.4.4.62.94.62,1.51s-.22,1.1-.62,1.5-.94.62-1.5.62Zm59.23,0c-.57,0-1.1-.22-1.5-.62-.4-.4-.62-.94-.62-1.5s.22-1.1.62-1.5c.81-.8,2.21-.8,3.01,0,.4.4.62.94.62,1.51s-.22,1.1-.62,1.51c-.4.4-.94.62-1.51.62Zm-65.35-9.71c-.57,0-1.1-.22-1.5-.62-.4-.4-.62-.94-.62-1.5s.22-1.1.62-1.51c.8-.8,2.21-.8,3.01,0,.39.39.61.92.62,1.47v.06c0,.56-.23,1.09-.63,1.48-.4.4-.93.62-1.5.62Zm71.47,0c-.57,0-1.11-.22-1.51-.62s-.61-.92-.62-1.48c0-.59.22-1.13.62-1.53.81-.81,2.21-.8,3.01,0,.4.4.62.94.62,1.51s-.22,1.1-.62,1.5c-.4.4-.94.62-1.5.62Zm-30.85-18.72c-.57,0-1.1-.22-1.5-.62-.4-.4-.62-.94-.62-1.5s.23-1.11.63-1.5c.8-.8,2.21-.8,3.01,0h0c.4.4.62.94.62,1.51s-.22,1.1-.62,1.5-.94.62-1.5.62Zm20.42-2.98c-.57,0-1.11-.22-1.51-.62s-.61-.91-.62-1.46h0c0-.61.22-1.14.62-1.55.8-.8,2.21-.8,3.01,0,.4.4.62.94.62,1.51s-.22,1.1-.62,1.5-.94.62-1.5.62Zm-50.73,0c-.57,0-1.1-.22-1.51-.62-.4-.4-.62-.94-.62-1.51s.22-1.1.62-1.51c.81-.8,2.21-.8,3.01,0,.39.39.61.91.62,1.46h0c0,.62-.21,1.14-.62,1.55-.4.4-.93.62-1.5.62Zm20.55-3.09c-.57,0-1.1-.22-1.5-.62s-.62-.94-.62-1.5.22-1.1.62-1.51c.81-.8,2.22-.8,3.01,0,.4.4.62.94.62,1.5s-.22,1.1-.62,1.51c-.4.4-.94.62-1.51.62Z"/></svg>
```

## public/vercel.svg
```
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1155 1000"><path d="m577.3 0 577.4 1000H0z" fill="#fff"/></svg>
```

## public/next.svg
```
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 394 80"><path fill="#000" d="M262 0h68.5v12.7h-27.2v66.6h-13.6V12.7H262V0ZM149 0v12.7H94v20.4h44.3v12.6H94v21h55v12.6H80.5V0h68.7zm34.3 0h-17.8l63.8 79.4h17.9l-32-39.7 32-39.6h-17.9l-23 28.6-23-28.6zm18.3 56.7-9-11-27.1 33.7h17.8l18.3-22.7z"/><path fill="#000" d="M81 79.3 17 0H0v79.3h13.6V17l50.2 62.3H81Zm252.6-.4c-1 0-1.8-.4-2.5-1s-1.1-1.6-1.1-2.6.3-1.8 1-2.5 1.6-1 2.6-1 1.8.3 2.5 1a3.4 3.4 0 0 1 .6 4.3 3.7 3.7 0 0 1-3 1.8zm23.2-33.5h6v23.3c0 2.1-.4 4-1.3 5.5a9.1 9.1 0 0 1-3.8 3.5c-1.6.8-3.5 1.3-5.7 1.3-2 0-3.7-.4-5.3-1s-2.8-1.8-3.7-3.2c-.9-1.3-1.4-3-1.4-5h6c.1.8.3 1.6.7 2.2s1 1.2 1.6 1.5c.7.4 1.5.5 2.4.5 1 0 1.8-.2 2.4-.6a4 4 0 0 0 1.6-1.8c.3-.8.5-1.8.5-3V45.5zm30.9 9.1a4.4 4.4 0 0 0-2-3.3 7.5 7.5 0 0 0-4.3-1.1c-1.3 0-2.4.2-3.3.5-.9.4-1.6 1-2 1.6a3.5 3.5 0 0 0-.3 4c.3.5.7.9 1.3 1.2l1.8 1 2 .5 3.2.8c1.3.3 2.5.7 3.7 1.2a13 13 0 0 1 3.2 1.8 8.1 8.1 0 0 1 3 6.5c0 2-.5 3.7-1.5 5.1a10 10 0 0 1-4.4 3.5c-1.8.8-4.1 1.2-6.8 1.2-2.6 0-4.9-.4-6.8-1.2-2-.8-3.4-2-4.5-3.5a10 10 0 0 1-1.7-5.6h6a5 5 0 0 0 3.5 4.6c1 .4 2.2.6 3.4.6 1.3 0 2.5-.2 3.5-.6 1-.4 1.8-1 2.4-1.7a4 4 0 0 0 .8-2.4c0-.9-.2-1.6-.7-2.2a11 11 0 0 0-2.1-1.4l-3.2-1-3.8-1c-2.8-.7-5-1.7-6.6-3.2a7.2 7.2 0 0 1-2.4-5.7 8 8 0 0 1 1.7-5 10 10 0 0 1 4.3-3.5c2-.8 4-1.2 6.4-1.2 2.3 0 4.4.4 6.2 1.2 1.8.8 3.2 2 4.3 3.4 1 1.4 1.5 3 1.5 5h-5.8z"/></svg>
```

## public/globe.svg
```
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><g clip-path="url(#a)"><path fill-rule="evenodd" clip-rule="evenodd" d="M10.27 14.1a6.5 6.5 0 0 0 3.67-3.45q-1.24.21-2.7.34-.31 1.83-.97 3.1M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.48-1.52a7 7 0 0 1-.96 0H7.5a4 4 0 0 1-.84-1.32q-.38-.89-.63-2.08a40 40 0 0 0 3.92 0q-.25 1.2-.63 2.08a4 4 0 0 1-.84 1.31zm2.94-4.76q1.66-.15 2.95-.43a7 7 0 0 0 0-2.58q-1.3-.27-2.95-.43a18 18 0 0 1 0 3.44m-1.27-3.54a17 17 0 0 1 0 3.64 39 39 0 0 1-4.3 0 17 17 0 0 1 0-3.64 39 39 0 0 1 4.3 0m1.1-1.17q1.45.13 2.69.34a6.5 6.5 0 0 0-3.67-3.44q.65 1.26.98 3.1M8.48 1.5l.01.02q.41.37.84 1.31.38.89.63 2.08a40 40 0 0 0-3.92 0q.25-1.2.63-2.08a4 4 0 0 1 .85-1.32 7 7 0 0 1 .96 0m-2.75.4a6.5 6.5 0 0 0-3.67 3.44 29 29 0 0 1 2.7-.34q.31-1.83.97-3.1M4.58 6.28q-1.66.16-2.95.43a7 7 0 0 0 0 2.58q1.3.27 2.95.43a18 18 0 0 1 0-3.44m.17 4.71q-1.45-.12-2.69-.34a6.5 6.5 0 0 0 3.67 3.44q-.65-1.27-.98-3.1" fill="#666"/></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h16v16H0z"/></clipPath></defs></svg>
```

## public/window.svg
```
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5" fill="#666"/></svg>
```

## public/curve-2.png.webp
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0x9d in position 24: invalid start byte
```

## public/curve-3.png.webp
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xeb in position 27: invalid continuation byte
```

## src/middleware.ts
```typescript
import createMiddleware from 'next-intl/middleware';
import {routing} from './i18n/routing';
 
export default createMiddleware(routing);
 
export const config = {
  // Match only internationalized pathnames
  matcher: ['/', '/(pt|en)/:path*']
};
```

## src/app/favicon.ico
```
Erro ao ler o arquivo: 'utf-8' codec can't decode byte 0xf8 in position 14: invalid start byte
```

## src/app/[locale]/layout.tsx
```
// src/app/[locale]/layout.tsx
import {NextIntlClientProvider} from 'next-intl';
import {getMessages} from 'next-intl/server';
import {notFound} from 'next/navigation';
import {routing} from '@/i18n/routing';
import { Metadata } from 'next';


import './globals.css'
 
export const metadata: Metadata = {
  title: 'IdeaForge DB: Como criar Micro SaaS lucrativos resolvendo problemas reais',
  description: 'Descubra oportunidades validadas de Micro SaaS através de análise de discussões autênticas nas redes sociais. Acesse nossa base com milhares de ideias de negócios já validadas pelo mercado. Economize mais de 100 horas de pesquisa e acelere sua jornada empreendedora.',
}

interface LocaleLayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export default async function LocaleLayout({
  children,
  params
}: LocaleLayoutProps) {
   const { locale } = await params;

  // Ensure that the incoming `locale` is valid
  if (!routing.locales.includes(locale as any)) {
    notFound();
  }
 
  // Providing all messages to the client
  // side is the easiest way to get started
  const messages = await getMessages();
 
  return (
    <html lang={locale} className='scroll-smooth'>
      <head>
            <link rel="icon" href="/favicon.ico" />
      </head>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

## src/app/[locale]/page.tsx
```
'use client'

import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { BottomSection } from "@/components/BottomSection";
import { Footer } from "@/components/Footer";
import { useState } from "react";
import { useTranslations } from "next-intl";
import { ValueProposition } from "@/components/ValueProposition";
import { Faq } from "@/components/faq";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { HowItWorks } from "@/components/HowItWorks";

 export default function HomePage() {
   const t = useTranslations('HeroComponent');
    
   const list_ideas = {
      "en": [
        {
          "id": 1,
          "name": "AnonBoost",
          "description": "A SaaS platform that analyzes trends and content performance for faceless brands, providing insights and tools for growth.",
          "diferenciais": [
            "Specialized for faceless brands"            ,
            "AI-powered content analysis"                ,
            "Personalized growth recommendations"        ,
            "Competitive analysis for anonymous accounts"
          ],
          "features": [
            "Trend identification for faceless niches"     ,
            "Content performance analysis"                 ,
            "Hashtag and keyword research"                 ,
            "Competitor activity tracking"                 ,
            "Personalized strategy recommendations"        ,
            "Automated posting suggestions"                ,
            "Content generation templates"                 ,
            "Engagement tracking"                          ,
            "Growth reporting"                             ,
            "Integration with major social media platforms"
          ],
          "implementacaoScore": "3/5",
          "marketViabilidadeScore": "75/100",
          "categoria": "Social Media Management"
        },
        {
          "id": 2,
          "name": "LLM Workflow Forge",
          "description": "A platform that allows users to create custom, focused niche workflows using LLMs, with capabilities for integrations, controlled output formats and protective system prompts.",
          "diferenciais": [
            "LLMs focused workflows"   ,
            "Output control options"   ,
            "Integration capabilities" ,
            "System prompt protections"
          ],
          "features": [
            "Customizable workflows for any niche",
            "Integration with data sources"       ,
            "Controlled output formats"           ,
            "System prompt injection protection"  ,
            "Multi-LLM API access"                ,
            "Collaboration for prompts"           ,
            "Analytics of usage"                  ,
            "History of outputs"                  ,
            "Template creation"                   ,
            "Secure data input"
          ],
          "implementacaoScore": "3/5",
          "marketViabilidadeScore": "75/100",
          "categoria": "Artificial Intelligence"
        },
        {
          "id": 3,
          "name": "Vertical AI SaaS",
          "description": "A platform offering vertical SaaS solutions tailored for specific industries, incorporating AI and machine learning to meet their distinct needs.",
          "diferenciais": [
            "Vertical SaaS approach"              ,
            "AI-powered tools"                    ,
            "Machine learning for specific needs" ,
            "Custom solutions based on user needs"
          ],
          "features": [
            "AI-driven solution for multiple verticals",
            "Specialized use-cases by area"            ,
            "Data analysis with ML"                    ,
            "Customizable model creation"              ,
            "Automation via API"                       ,
            "Reporting and analytics"                  ,
            "Integration with existing infrastructure" ,
            "User management and access control"       ,
            "Scalability and customization options"    ,
            "Security and data protection"
          ],
          "implementacaoScore": "4/5",
          "marketViabilidadeScore": "90/100",
          "categoria": "Artificial Intelligence"
        },
        {
          "id": 4,
          "name": "Global Income Bridge",
          "description": "A platform that automates the process of consolidating income from multiple international sources (like Stripe and App Stores), creates a monthly summary, and facilitates transfers to local companies. The SaaS would also provide a module to generate reports and compliance with different tax rules in different countries.",
          "diferenciais": [
            "Automation for international income",
            "Income summaries"                   ,
            "Local transfers"                    ,
            "Tax compliance for multi-region"
          ],
          "features": [
            "Multiple source integration via API"   ,
            "Automated income summaries"            ,
            "Local transfers according to tax rules",
            "Reporting by region and source"        ,
            "Tax compliance documentation"          ,
            "Integration with accounting tools"     ,
            "Multi-currency support"                ,
            "Payout management options"             ,
            "Data tracking and forecasting"         ,
            "User management and access control"
          ],
          "implementacaoScore": "3/5",
          "marketViabilidadeScore": "85/100",
          "categoria": "Fintech"
        }
      ],
      "pt": [
          {
            "id": 1,
            "name": "AnonBoost",
            "description": "Plataforma SaaS que analisa tendências e desempenho de conteúdo para marcas sem rosto, fornecendo insights e ferramentas para crescimento.",
            "diferenciais": [
              "Especializada para marcas sem rosto",
              "Análise de conteúdo com inteligência artificial",
              "Recomendações personalizadas para crescimento",
              "Análise competitiva para contas anônimas"
            ],
            "features": [
              "Identificação de tendências para nichos sem rosto",
              "Análise de desempenho de conteúdo",
              "Pesquisa de hashtags e palavras-chave",
              "Monitoramento de atividade de concorrentes",
              "Recomendações de estratégia personalizadas",
              " Sugestões de publicação automatizadas",
              "Modelos de geração de conteúdo",
              "Monitoramento de engajamento",
              "Relatórios de crescimento",
              "Integração com principais plataformas de mídias sociais"
            ],
            "implementacaoScore": "3/5",
            "marketViabilidadeScore": "75/100",
            "categoria": "Gestão de Mídias Sociais"
          },
          {
            "id": 2,
            "name": "LLM Workflow Forge",
            "description": "Plataforma que permite aos usuários criar fluxos de trabalho personalizados e focalizados para nichos específicos utilizando LLMs, com capacidades de integração, opções de formatação de saída controlada e proteção de prompts do sistema.",
            "diferenciais": [
              "Fluxos de trabalho focalizados em LLMs",
              "Opções de controle de saída",
              "Capacidades de integração",
              "Proteção de prompts do sistema"
            ],
            "features": [
              "Fluxos de trabalho personalizados para qualquer nicho",
              "Integração com fontes de dados",
              "Formatação de saída controlada",
              "Proteção de injectores de prompts",
              "Acesso à API de múltiplos LLMs",
              "Colaboração para prompts",
              "Análise de uso",
              "Histórico de saídas",
              "Criação de modelos",
              "Entrada de dados segura"
            ],
            "implementacaoScore": "3/5",
            "marketViabilidadeScore": "75/100",
            "categoria": "Inteligência Artificial"
          },
          {
            "id": 3,
            "name": "Vertical AI SaaS",
            "description": "Plataforma que oferece soluções SaaS verticais personalizadas para indústrias específicas, incorporando inteligência artificial e aprendizado de máquina para atender às suas necessidades únicas.",
            "diferenciais": [
              "Abordagem SaaS vertical",
              "Ferramentas com inteligência artificial",
              "Aprendizado de máquina para necessidades específicas",
              "Soluções personalizadas com base nas necessidades do usuário"
            ],
            "features": [
              "Solução com inteligência artificial para múltiplos verticais",
              "Uso-cases especializados por área",
              "Análise de dados com ML",
              "Criação de modelos personalizados",
              "Automatização via API",
              "Relatórios e análise",
              "Integração com infraestrutura existente",
              "Gerenciamento de usuário e controle de acesso",
              "Opções de escalabilidade e personalização",
              "Segurança e proteção de dados"
            ],
            "implementacaoScore": "4/5",
            "marketViabilidadeScore": "90/100",
            "categoria": "Inteligência Artificial"
          },
          {
            "id": 4,
            "name": "Global Income Bridge",
            "description": "Plataforma que automatiza o processo de consolidação de renda internacional de múltiplas fontes (como Stripe e Lojas de Aplicativos), cria um resumo mensal e facilita transferências para empresas locais. A SaaS também fornecerá um módulo para gerar relatórios e cumprir com as regras fiscais diferentes em diferentes países.",
            "diferenciais": [
              "Automatização de renda internacional",
              "Resumo de renda",
              "Transferências locais",
              "Cumprimento com regras fiscais multi-regional"
            ],
            "features": [
              "Integração via API com múltiplas fontes",
              "Resumo de renda automatizado",
              "Transferências locais de acordo com as regras fiscais",
              "Relatórios por região e fonte",
              "Documentação de cumprimento com regras fiscais",
              "Integração com ferramentas de contabilidade",
              "Suporte a múltiplas moedas",
              "Gerenciamento de pagamentos",
              "Monitoramento e previsão de dados",
              "Gerenciamento de usuário e controle de acesso"
            ],
            "implementacaoScore": "3/5",
            "marketViabilidadeScore": "85/100",
            "categoria": "Fintech"
          }
      ]
    }

    const lang = String(t('ideas')) as 'en' | 'pt';
    const ideas = list_ideas[lang];
    
    const handlePreviousIdea = () => {
        if (currentIdeaIndex > 0) {
            setCurrentIdeaIndex(currentIdeaIndex - 1);
          }
      };

    const handleNextIdea = () => {
        if (currentIdeaIndex < ideas.length - 1) {
            setCurrentIdeaIndex(currentIdeaIndex + 1);
          }
    };
  
  const [currentIdeaIndex, setCurrentIdeaIndex] = useState(0);
  
     return (
         <div> 
            <Header />
            <Hero />
            <ValueProposition />
            <HowItWorks />
            {/* <h2 className="text-2xl md:text-4xl font-bold mt-20 text-center">
                  {t('hero_ideias_title_part1')} <br />
                  <span className="bg-blue-600 text-white px-2 py-1 rounded leading-normal">{t('hero_ideias_title_part2')}</span>
                </h2>
                
                <IdeaCard
                    idea={ideas[currentIdeaIndex]}
                    onPrevious={handlePreviousIdea}
                    onNext={handleNextIdea}
                    disableNextButton={currentIdeaIndex === ideas.length - 1}
                    disablePrevButton={currentIdeaIndex === 0}
                /> */}
            {/* <FeaturesSection /> */}
            {/* <PriceSection /> */}
            {/* <WaitlistBenefitsSection />  */}
            <TestimonialsSection />
            <Faq />
            
            <BottomSection />
            <Footer />
        </div>
   );
}
```

## src/app/[locale]/globals.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: Arial, Helvetica, sans-serif;
}

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    --secondary: 0 0% 96.1%;
    --secondary-foreground: 0 0% 9%;
    --muted: 0 0% 96.1%;
    --muted-foreground: 0 0% 45.1%;
    --accent: 0 0% 96.1%;
    --accent-foreground: 0 0% 9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 89.8%;
    --input: 0 0% 89.8%;
    --ring: 0 0% 3.9%;
    --chart-1: 12 76% 61%;
    --chart-2: 173 58% 39%;
    --chart-3: 197 37% 24%;
    --chart-4: 43 74% 66%;
    --chart-5: 27 87% 67%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    --card: 0 0% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 0 0% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 0 0% 9%;
    --secondary: 0 0% 14.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 0 0% 14.9%;
    --muted-foreground: 0 0% 63.9%;
    --accent: 0 0% 14.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 0 0% 14.9%;
    --input: 0 0% 14.9%;
    --ring: 0 0% 83.1%;
    --chart-1: 220 70% 50%;
    --chart-2: 160 60% 45%;
    --chart-3: 30 80% 55%;
    --chart-4: 280 65% 60%;
    --chart-5: 340 75% 55%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}

```

## src/app/[locale]/dashboard/ideas/page.tsx
```
// src/app/[locale]/dashboard/ideas/page.tsx
"use client";

import { useState, useEffect } from 'react';
import { IdeasTable } from '@/components/IdeasTable';
import { Pagination } from '@/components/Pagination';
import { IdeasFilter } from '@/components/IdeasFilter';
import { useSearchParams } from 'next/navigation';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';

interface SaasIdea {
    id: number;
    name: string;
    description: string | null;
    differentiators: string[] | null;
    features: string[] | null;
    implementation_score: number | null;
    market_viability_score: number | null;
    category: string | null;
    post_id: string;
}

interface PaginatedResponse {
  items: SaasIdea[];
  total: number;
  page: number;
  page_size: number;
}

type OrderDirection = 'asc' | 'desc';
type OrderBy = 'implementation_score' | 'market_viability_score' | 'category' | null;


export default function IdeasPage() {
  const searchParams = useSearchParams();
  const [ideas, setIdeas] = useState<SaasIdea[]>([]);
  const [total, setTotal] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
   const [orderBy, setOrderBy] = useState<OrderBy>(null);
    const [orderDirection, setOrderDirection] = useState<OrderDirection>('asc');
     const [filters, setFilters] = useState<{
         category?: string | null;
        description?: string | null;
    }>({});

  const fetchIdeas = async () => {
        const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}/saas_ideas`);

        Object.entries({
             page: currentPage,
            page_size: pageSize,
            ...filters,
            order_by: orderBy,
             order_direction: orderDirection,
        }).forEach(([key, value]) => {
            if (value != null) {
              url.searchParams.append(key, String(value));
            }
         });


    try {
       const response = await fetch(url.toString());
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data: PaginatedResponse = await response.json();

        setIdeas(data.items);
        setTotal(data.total);

    } catch (error) {
      console.error("Error fetching data:", error);
    //TODO: adicionar feedback para o usuário
    }
  };


    useEffect(() => {
        fetchIdeas();
    }, [currentPage, pageSize, filters, orderBy, orderDirection]);

    const handlePageChange = (page: number) => {
      setCurrentPage(page);
    };

    const handlePageSizeChange = (size: number) => {
      setPageSize(size);
      setCurrentPage(1);
    };

    const handleFilterChange = (newFilters: any) => {
         setFilters(newFilters);
         setCurrentPage(1);
    };
    const handleSortChange = (field: OrderBy) => {
         if (orderBy === field) {
             setOrderDirection(orderDirection === 'asc' ? 'desc' : 'asc');
        } else {
            setOrderBy(field);
             setOrderDirection('asc');
        }
   };


  return (
    <div>
        <Header />
        <div className="container mx-auto py-8">
            <h2 className="text-2xl font-bold mb-4">Ideias de SaaS</h2>
            <IdeasFilter onFilterChange={handleFilterChange} />
            <IdeasTable
                ideas={ideas}
                    onSortChange={handleSortChange}
                orderBy={orderBy}
                orderDirection={orderDirection}
            />
            <Pagination
                    currentPage={currentPage}
                pageSize={pageSize}
                totalItems={total}
                onPageChange={handlePageChange}
                onPageSizeChange={handlePageSizeChange}
            />
        </div>
        <Footer />
      </div>
  );
}
```

## src/components/Hero.tsx
```
'use client';
// src/components/Hero.tsx
import { useTranslations } from "next-intl";
import { EmailCaptureForm } from "./EmailCaptureForm";
import Image from 'next/image';

export function Hero() {
    const t = useTranslations('HeroComponent');

    return (
        <section className="py-10 z-10">
            <div className="container mx-auto flex flex-col md:flex-row items-center gap-8">
                {/* Coluna Esquerda (Texto e Formulário) */}
                <div className="md:w-1/2">
                     <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 relative z-10 leading-tight text-center md:text-left">
                        {t('hero_title_part1')} <br /> {t('hero_title_part2')} <span className="bg-blue-600 text-white px-2 py-1 rounded leading-normal">{t('hero_title_part3')}</span>
                    </h1>
                     <p className="text-sm md:text-base text-gray-500 mb-4 md:mb-8 text-center md:text-left">
                        {t('hero_subtitle_part1')} <br /> {t('hero_subtitle_part2')}
                     </p>
                    <div className="container mx-auto text-center md:text-left">
                        <EmailCaptureForm buttonText={t('call_to_action')} buttonVariant="default" buttonSize="default" className="bg-blue-600" />
                    </div>
                </div>

               {/* Coluna Direita (Vídeo) */}
                <div className="md:w-1/2 flex items-center justify-center z-50">
                    <div className="max-w-md w-full aspect-video">
                        <Image
                            src="/hero.webp" // Caminho para a sua imagem
                            alt="Ícone de IA" // Texto alternativo para acessibilidade
                            width={500}     // Largura da imagem
                            height={500}    // Altura da imagem
                            priority
                        />
                        {/* <video
                            src="/video-demo.mp4"
                            autoPlay
                            loop
                            muted
                            className="w-full rounded-lg"
                        /> */}
                     </div>
                </div>
            </div>
            {/* <DiscountSection /> */}
        </section>
    );
}
```

## src/components/IdeaDetailsDialog.tsx
```
// src/components/IdeaDetailsDialog.tsx
import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface SaasIdea {
    id: number;
    name: string;
    description: string | null;
    differentiators: string[] | null;
    features: string[] | null;
    implementation_score: number | null;
    market_viability_score: number | null;
    category: string | null;
    post_id: string;
}


interface IdeaDetailsDialogProps {
    idea: SaasIdea;
    open: boolean;
     onClose: () => void;
}

export function IdeaDetailsDialog({ idea, open, onClose }: IdeaDetailsDialogProps) {
    if (!idea) return null;

  return (
      <Dialog open={open} onOpenChange={onClose}>
          <DialogContent className="max-h-[80vh] overflow-y-auto w-[90vw] max-w-2xl">
                <DialogHeader>
                  <DialogTitle>{idea.name}</DialogTitle>
              </DialogHeader>
                <div className="bg-gray-100 p-4 rounded-md mb-4">
                  <h3 className="text-lg font-semibold mb-2">Description:</h3>
                       <p>{idea.description || 'No description provided'}</p>
                 </div>
                 <div className="bg-gray-100 p-4 rounded-md mb-4">
                     <h3 className="text-lg font-semibold mb-2">Differentials:</h3>
                       {idea.differentiators && idea.differentiators.length > 0 ? (
                            <ul className="list-disc pl-4">
                                {idea.differentiators.map((diff, i) => (
                                    <li key={i}>{diff}</li>
                                ))}
                             </ul>
                       ) : <p>No differentials provided</p>
                     }
                </div>
                <div className="bg-gray-100 p-4 rounded-md mb-4">
                   <h3 className="text-lg font-semibold mb-2">Features:</h3>
                      {idea.features && idea.features.length > 0 ? (
                          <ul className="list-disc pl-4">
                            {idea.features.map((feat, i) => (
                                  <li key={i}>{feat}</li>
                                ))}
                             </ul>
                           ) : <p>No features provided</p>
                         }
                </div>
                 <div className="bg-gray-100 p-4 rounded-md mb-4">
                       <h3 className="text-lg font-semibold mb-2">Category:</h3>
                        <p>{idea.category || 'No category'}</p>
                   </div>
                   <div className="bg-gray-100 p-4 rounded-md mb-4">
                     <h3 className="text-lg font-semibold mb-2">Implementation Score:</h3>
                    <p>{idea.implementation_score || 'Not available'}</p>
                 </div>
                 <div className="bg-gray-100 p-4 rounded-md mb-4">
                    <h3 className="text-lg font-semibold mb-2">Market Viability Score:</h3>
                     <p>{idea.market_viability_score || 'Not available'}</p>
                </div>
         </DialogContent>
      </Dialog>
  );
}
```

## src/components/Pagination.tsx
```
// src/components/Pagination.tsx
import React from 'react';
import { Button } from '@/components/ui/button';

interface PaginationProps {
    currentPage: number;
    pageSize: number;
    totalItems: number;
    onPageChange: (page: number) => void;
    onPageSizeChange: (size: number) => void;
}

export function Pagination({
    currentPage,
    pageSize,
    totalItems,
    onPageChange,
    onPageSizeChange
}: PaginationProps) {
   const totalPages = Math.ceil(totalItems / pageSize);

    const handlePrevious = () => {
        if (currentPage > 1) {
           onPageChange(currentPage - 1);
      }
    };

   const handleNext = () => {
        if (currentPage < totalPages) {
            onPageChange(currentPage + 1);
      }
   };


    const handlePageSize = (size: number) => {
        onPageSizeChange(size)
    }

    return (
        <div className="flex justify-between items-center mt-6">
            <div className="flex items-center gap-2">
               <Button variant="outline" onClick={handlePrevious} disabled={currentPage === 1}>Anterior</Button>
                <Button variant="outline" onClick={handleNext} disabled={currentPage === totalPages}>Próxima</Button>
            </div>
           <div className="flex items-center gap-2">
              <span className="text-sm text-gray-500">Itens por página:</span>
               <select
                    className="border border-gray-300 rounded px-2 py-1 text-sm text-gray-700"
                    value={pageSize}
                   onChange={(e) => handlePageSize(Number(e.target.value))}
              >
                  <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
               </select>
            </div>
            <span className="text-sm text-gray-500">
                 Página {currentPage} de {totalPages}
           </span>
       </div>
    );
}
```

## src/components/StepNumber.tsx
```
// src/components/StepNumber.tsx
import React from 'react';
import { cn } from '@/lib/utils';

interface StepNumberProps {
    number: number;
    bgColor?: string;
}

export function StepNumber({ number, bgColor }: StepNumberProps) {
    return (
        <span className={cn("rounded-full flex items-center justify-center text-white font-semibold text-sm", bgColor)} style={{width: '32px', height: '32px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center',}}>
           {number}
         </span>
    );
}
```

## src/components/PriceSection.tsx
```
// src/components/PriceSection.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useTranslations } from "next-intl";
import { DiscountSection } from "./DiscountSection";
import Image from 'next/image';

export function PriceSection() {
    const t = useTranslations('PriceSection');

    return (
        <section className="py-16 relative">
            <Image
                            src="/curve-3.png.webp"
                            alt="Curve Left"
                            width={379}
                            height={748}
                            className="absolute top-0 right-0 z-0 pointer-events-none"
                            priority
                            />
                <div className="container mx-auto text-center">
                    <h2 className="text-2xl md:text-3xl lg:text-5xl font-bold mb-4">
                        {t('title_part_1')} <br /> {t('title_part_2')}
                    </h2>
                    <DiscountSection />
                    <div className="ml-2 mr-2">
                        <Card className="max-w-md mx-auto p-6 border">
                            <CardHeader>
                                <CardTitle className="text-2xl text-blue-500 font-bold">{t('card_tile_1')}</CardTitle>
                                <span className="text-gray-500 line-through">{t('card_full_price')}</span>
                                <span className="text-4xl font-bold">{t('card_discount_price')}</span>
                                    <CardDescription>{t('card_description')}</CardDescription>
                            </CardHeader>
                            <CardContent className="text-left mt-4">
                                <ul className="list-disc pl-4">
                                    <li className="mb-2">{t('card_feature_1')}</li>
                                    <li className="mb-2">{t('card_feature_2')}</li>
                                    <li className="mb-2">{t('card_feature_3')}</li>
                                    <li className="mb-2">{t('card_feature_4')}</li>
                                    <li className="mb-2">{t('card_feature_5')}</li>
                                </ul>
                                <Button className="w-full mt-4 bg-blue-600" size="lg">{t('call_to_action')}</Button>
                            </CardContent>
                        </Card>
                    </div>  
               </div>
           </section>
        // <section className="py-16">
        //     <div className="container mx-auto text-center">
        //         <h2 className="text-5xl font-bold mb-8">Don't waste time on boring things. <br /> Get profitable really fast</h2>
        //         <DiscountSection />
        //         <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

        //         <Card className="max-w-md mx-auto p-6 border">
        //                 <CardHeader>
        //                     <CardTitle className="text-2xl text-blue-500 font-bold">All-in</CardTitle>
        //                     <span className="text-gray-500 line-through">$199</span>
        //                     <span className="text-4xl font-bold">$99</span>
        //                     <CardDescription>Pay once. Build unlimited products</CardDescription>
        //                 </CardHeader>
        //                 <CardContent className="text-left mt-4">
        //                     <ul className="list-disc pl-4">
        //                     <li className="mb-2">NextJS boilerplate</li>
        //                     <li className="mb-2">SEO Optimization</li>
        //                     <li className="mb-2">Ready for multi-tenancy & collaboration</li>
        //                     <li className="mb-2">Prisma as ORM</li>
        //                         <li className="mb-2">Stripe as payment processor</li>
        //                     <li className="mb-2">Google, Github & Magic Link authentication</li>
        //                     <li className="mb-2">Components & animations</li>
        //                         <li className="mb-2">Lifetime updates</li>
        //                     </ul>
        //                     <Button className="w-full mt-4 bg-blue-600" size="lg">Get TurboStack</Button>
        //             </CardContent>
        //             </Card>
        //             {/* <Card className="p-6 border opacity-50 pointer-events-none relative">
        //                 <div className="absolute top-4 left-4 bg-red-500 text-white text-xs py-1 px-2 rounded-md">Em Breve</div>
        //                 <CardHeader>
        //                     <CardTitle className="text-2xl text-blue-500 font-bold">Standard</CardTitle>
        //                     <span className="text-gray-500 line-through">$299</span>
        //                     <span className="text-4xl font-bold">$149</span>
        //                         <CardDescription>Monthly. Build unlimited products</CardDescription>
        //                 </CardHeader>
        //                 <CardContent className="text-left mt-4">
        //                 <ul className="list-disc pl-4">
        //                     <li className="mb-2">Atualizações diárias com novos insights de mercado</li>
        //                     <li className="mb-2">SEO Optimization</li>
        //                         <li className="mb-2">Ready for multi-tenancy & collaboration</li>
        //                     <li className="mb-2">Prisma as ORM</li>
        //                     <li className="mb-2">Stripe as payment processor</li>
        //                         <li className="mb-2">Google, Github & Magic Link authentication</li>
        //                         <li className="mb-2">Components & animations</li>
        //                         <li className="mb-2">Lifetime updates</li>
        //                     </ul>
        //                 <Button className="w-full mt-4 bg-blue-600" size="lg">Get TurboStack</Button>
        //             </CardContent>
        //                 </Card>
        //             <Card className="p-6 border opacity-50 pointer-events-none relative">
        //                 <div className="absolute top-4 left-4 bg-red-500 text-white text-xs py-1 px-2 rounded-md">Em Breve</div>
        //                 <CardHeader>
        //                         <CardTitle className="text-2xl text-blue-500 font-bold">Premium</CardTitle>
        //                         <span className="text-gray-500 line-through">$399</span>
        //                         <span className="text-4xl font-bold">$199</span>
        //                         <CardDescription>Monthly. Build unlimited products</CardDescription>
        //                     </CardHeader>
        //                     <CardContent className="text-left mt-4">
        //                         <ul className="list-disc pl-4">
        //                                 <li className="mb-2">NextJS boilerplate</li>
        //                             <li className="mb-2">SEO Optimization</li>
        //                                 <li className="mb-2">Ready for multi-tenancy & collaboration</li>
        //                             <li className="mb-2">Prisma as ORM</li>
        //                                 <li className="mb-2">Stripe as payment processor</li>
        //                                 <li className="mb-2">Google, Github & Magic Link authentication</li>
        //                                 <li className="mb-2">Components & animations</li>
        //                                 <li className="mb-2">Lifetime updates</li>
        //                             </ul>
        //                         <Button className="w-full mt-4 bg-blue-600" size="lg">Get TurboStack</Button>
        //                     </CardContent>
        //                     </Card> */}
        //             </div>
        //     </div>
        // </section>
    );
}
```

## src/components/IdeasTable.tsx
```
// src/components/IdeasTable.tsx
import React, { useState } from 'react';
import { ArrowDown, ArrowUp } from 'lucide-react';
import { RatingStars } from './RatingStars';
import { Button } from '@/components/ui/button';
import { IdeaDetailsDialog } from '@/components/IdeaDetailsDialog';


interface SaasIdea {
  id: number;
  name: string;
  description: string | null;
  differentiators: string[] | null;
  features: string[] | null;
  implementation_score: number | null;
  market_viability_score: number | null;
  category: string | null;
  post_id: string;
}

type OrderDirection = 'asc' | 'desc';
type OrderBy = 'implementation_score' | 'market_viability_score' | 'category' | null;

interface IdeasTableProps {
    ideas: SaasIdea[];
    onSortChange: (field: OrderBy) => void;
    orderBy: OrderBy;
    orderDirection: OrderDirection;
}

export function IdeasTable({ ideas, onSortChange, orderBy, orderDirection }: IdeasTableProps) {
    const handleSort = (field: OrderBy) => {
         onSortChange(field);
    };

    const [selectedIdea, setSelectedIdea] = useState<SaasIdea | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const openDialog = (idea: SaasIdea) => {
    setSelectedIdea(idea);
    setIsDialogOpen(true);
  };

  const closeDialog = () => {
    setIsDialogOpen(false);
  };
    
  return (
        <div className="overflow-x-auto">
            <table className="min-w-[1000px] leading-normal">
                <thead>
                <tr className="bg-gray-100 text-gray-600">
                    <th className="px-5 py-3 text-left text-xs font-semibold uppercase">ID</th>
                    <th className="px-5 py-3 text-left text-xs font-semibold uppercase">Name</th>
                     <th className="px-5 py-3 text-left text-xs font-semibold uppercase">Description</th>
                     <th className="px-5 py-3 text-left text-xs font-semibold uppercase cursor-pointer" onClick={() => handleSort('category')}>
                        <div className="flex items-center gap-1">
                           Category
                           {orderBy === 'category' && (
                                 orderDirection === 'asc' ? <ArrowUp className='h-4 w-4' /> :  <ArrowDown className='h-4 w-4'/>
                            )}
                          </div>
                     </th>
                    <th className="px-5 py-3 text-left text-xs font-semibold uppercase cursor-pointer" onClick={() => handleSort('implementation_score')}>
                         <div className="flex items-center gap-1">
                            Implementation Score
                           {orderBy === 'implementation_score' && (
                                 orderDirection === 'asc' ? <ArrowUp className='h-4 w-4' /> : <ArrowDown className='h-4 w-4'/>
                            )}
                           </div>
                      </th>
                     <th className="px-5 py-3 text-left text-xs font-semibold uppercase cursor-pointer" onClick={() => handleSort('market_viability_score')}>
                        <div className="flex items-center gap-1">
                            Market Viability Score
                             {orderBy === 'market_viability_score' && (
                                   orderDirection === 'asc' ? <ArrowUp className='h-4 w-4' /> : <ArrowDown className='h-4 w-4'/>
                                )}
                           </div>
                      </th>
                     <th className="px-5 py-3 text-left text-xs font-semibold uppercase">Actions</th>
                 </tr>
                </thead>
                <tbody>
                {ideas.map(idea => (
                    <tr key={idea.id} className="border-b border-gray-200 hover:bg-gray-50">
                        <td className="px-5 py-5 text-sm">{idea.id}</td>
                         <td className="px-5 py-5 text-sm">{idea.name}</td>
                         <td className="px-5 py-5 text-sm">{idea.description}</td>
                        <td className="px-5 py-5 text-sm">{idea.category}</td>
                        <td className="px-5 py-5 text-sm">
                            <RatingStars score={idea.implementation_score} size={18} />
                         </td>
                        <td className="px-5 py-5 text-sm">{idea.market_viability_score}</td>
                        <td className="px-5 py-5 text-sm">
                            <Button variant="outline" size="sm" onClick={() => openDialog(idea)}>Details</Button>
                         </td>
                    </tr>
                  ))}
                </tbody>
            </table>
              {selectedIdea && (
                    <IdeaDetailsDialog
                        idea={selectedIdea}
                        open={isDialogOpen}
                        onClose={closeDialog}
                   />
               )}
        </div>
    );
}
```

## src/components/BottomSection.tsx
```
// src/components/BottomSection.tsx



import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useTranslations } from "next-intl";
import { saveNewsletterEmail } from "@/lib/newsletter-service";
import { useState } from "react";
import { Mail } from 'lucide-react';

interface FormState {
    loading: boolean;
    success: boolean | null;
    error: string | null;
}

async function handleSubmit(prevState: FormState, formData: FormData): Promise<FormState> {
    const email = formData.get('email') as string;

    if (!email) {
        return {
          loading: false,
          success: false,
          error: 'Por favor, insira seu e-mail.',
        };
      }

    try {
        await saveNewsletterEmail(email);
        return {
            loading: false,
            success: true,
            error: null,
        };
    } catch (e:any) {
        return {
          loading: false,
          success: false,
          error: 'Ocorreu um erro ao salvar seu e-mail, por favor tente novamente.',
        };
      }
}


export function BottomSection() {
  const t = useTranslations('bottomSection');
    const [state, setState] = useState<FormState>({
        loading: false,
        success: null,
        error: null,
    });

  return (
    <section className="bg-blue-600 py-16 text-white text-center">
      <div className="container mx-auto px-4"> {/* Adicionando px-4 aqui */}
        <h2 className="text-2xl md:text-3xl lg:text-5xl font-bold mb-4 ml-4 mr-4">
            {t('title')}
         </h2>
        <p className="text-base md:text-lg mb-8 md:mb-8 text-center">
            {t('sub-title')}
       </p>
       <form action={async (formData) => {
            const newState = await handleSubmit(state, formData);
            setState(newState);
            }
        } className="flex flex-col md:flex-row items-center justify-center gap-4">
        <div className="relative w-full md:w-auto">
         <Input
             type="email"
             name="email"
              placeholder="Seu e-mail"
              required
             disabled={state.loading || state.success === true}
            className="text-white placeholder:text-white placeholder-opacity-70 pr-10 md:w-64"
           />
          <Mail className="absolute right-3 top-2.5 h-5 w-5 text-white pointer-events-none" />
        </div>
          <Button type="submit" size="lg" variant="secondary" disabled={state.loading || state.success === true}>
                {state.loading ? 'Enviando...' : state.success === true ? 'Enviado!' : t('call_to_action')}
           </Button>
       </form>
        {state.success === false && <p className="text-red-300 mt-4">{state.error}</p>}
      </div>
    </section>
  );
}
```

## src/components/ClientPhoneInput.tsx
```
// src/components/ClientPhoneInput.tsx
'use client';
import PhoneInput from 'react-phone-number-input';
import 'react-phone-number-input/style.css';
import { useState } from 'react';

interface ClientPhoneInputProps {
  placeholder: string;
  defaultCountry: 'BR' | 'US';
  className: string;
  name: string;
  onChange: (value: string | undefined) => void;
}

export function ClientPhoneInput({ placeholder, defaultCountry, className, name, onChange }: ClientPhoneInputProps) {
  const [phone, setPhone] = useState<string | undefined>(undefined);

  const handlePhoneChange = (value: string | undefined) => {
    setPhone(value);
     onChange(value);
  };

  return (
    <PhoneInput
        placeholder={placeholder}
        value={phone}
        onChange={handlePhoneChange}
        defaultCountry={defaultCountry}
        name={name}
        className={className}
    />
  );
}
```

## src/components/HowItWorks.tsx
```
// src/components/HowItWorks.tsx
import React from 'react';
import { useTranslations } from "next-intl";
import { StepNumber } from './StepNumber';

interface InfoCardProps {
    title: string;
    description: string;
    stepNumber: number;
    bgColor?: string;
}

const InfoCard = ({ title, description, stepNumber, bgColor }: InfoCardProps) => {
    return (
        <div className="flex items-start gap-4 mb-6">
             <div style={{display: 'inline-flex', alignItems: 'flex-start', justifyContent: 'flex-start'}}>
              <StepNumber number={stepNumber} bgColor={bgColor} />
             </div>
            <div>
                <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
                <p className="text-gray-600 text-sm">{description}</p>
            </div>
        </div>
    );
};

export function HowItWorks() {
    const t = useTranslations("HowItWorks");
    return (
        <section className="py-16">
            <div className="container mx-auto">
                <div className="text-center mb-8">
                     <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-2 text-gray-800">
                            {t('title')}
                        </h2>
                    <p className="text-base md:text-lg text-gray-600">
                    {t('sub-title')}
                   </p>
                 </div>
                <div className="flex flex-col md:flex-row items-center gap-8">
                    {/* Coluna Esquerda (Vídeo) */}
                    <div className="md:w-1/2 flex items-center justify-center z-50">
                        <div className="max-w-md w-full aspect-video">
                            <video
                                src="/video-demo.mp4"
                                autoPlay
                                loop
                                muted
                                className="w-full rounded-lg"
                            />
                        </div>
                    </div>

                    {/* Coluna Direita (Tópicos) */}
                    <div className="md:w-1/2">
                        <InfoCard
                            title={t('feature_title_1')}
                            description={t('feature_description_1')}
                            stepNumber={1}
                            bgColor='bg-yellow-500'
                        />
                        <InfoCard
                            title={t('feature_title_2')}
                            description={t('feature_description_2')}
                           stepNumber={2}
                           bgColor='bg-blue-500'
                        />
                        <InfoCard
                            title={t('feature_title_3')}
                            description={t('feature_description_3')}
                            stepNumber={3}
                            bgColor='bg-gray-500'
                        />
                         <InfoCard
                            title={t('feature_title_4')}
                            description={t('feature_description_4')}
                            stepNumber={4}
                           bgColor='bg-green-500'
                        />
                        <InfoCard
                            title={t('feature_title_5')}
                            description={t('feature_description_5')}
                             stepNumber={5}
                            bgColor='bg-red-500'
                        />
                    </div>
                </div>
            </div>
        </section>
    );
}
```

## src/components/RatingStars.tsx
```
// src/components/RatingStars.tsx
import React from 'react';
import { Star } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RatingStarsProps {
  score: number | null;
  maxScore?: number;
  size?: string | number;
  className?: string;
}

export function RatingStars({ score, maxScore = 5, size = 20, className }: RatingStarsProps) {
  const filledStars = score ? Math.round(score) : 0;
  const emptyStars = maxScore - filledStars;

  return (
      <div className={cn("flex items-center", className)}>
        {Array.from({ length: filledStars }, (_, i) => (
            <Star key={i} size={size} fill="currentColor" className='text-yellow-400'/>
         ))}
        {Array.from({ length: emptyStars }, (_, i) => (
          <Star key={`empty-${i}`} size={size} className='text-gray-300'/>
        ))}
    </div>
    );
}
```

## src/components/IdeasFilter.tsx
```
// src/components/IdeasFilter.tsx
import React, { useState, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { cn } from '@/lib/utils';

interface IdeasFilterProps {
    onFilterChange: (filters: any) => void;
}

export function IdeasFilter({ onFilterChange }: IdeasFilterProps) {
  const [category, setCategory] = useState<string | null>(null);
    const [description, setDescription] = useState<string | null>(null);
    const [categories, setCategories] = useState<string[]>([]);

    const fetchCategories = async () => {
       try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/saas_categories`);
           if (!response.ok) {
             throw new Error(`HTTP error! Status: ${response.status}`);
           }
           const data: string[] = await response.json();
           setCategories(data);
       } catch (error) {
           console.error("Error fetching categories:", error);
           // TODO: Adicionar feedback para o usuário
       }
   };

    useEffect(() => {
         fetchCategories();
    }, []);

    const handleApplyFilters = () => {
       onFilterChange({
            category: category,
            description: description,
        });
    };

    const handleClearFilters = () => {
        setCategory(null);
        setDescription(null);
         onFilterChange({});
    };


  return (
        <div className="flex flex-col gap-4 mb-6">
            <div className="flex md:flex-row gap-4 items-end">
                <div className="w-1/4">
                    <Select onValueChange={setCategory} >
                        <SelectTrigger className="w-full">
                            <SelectValue placeholder="Category" />
                        </SelectTrigger>
                        <SelectContent>
                              {categories.map((category) => (
                                <SelectItem key={category} value={category}>
                                  {category}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                </div>
               <div className="flex-1">
                     <Input
                            type="text"
                            placeholder="Description"
                            value={description ?? ''}
                            onChange={(e) => setDescription(e.target.value === '' ? null : e.target.value)}
                            className="text-black"
                       />
                </div>
                <div className="flex gap-2">
                   <Button variant="outline" onClick={handleApplyFilters} className="whitespace-nowrap">Aplicar</Button>
                   <Button variant="outline" onClick={handleClearFilters} className="whitespace-nowrap">Limpar</Button>
                 </div>
          </div>
       </div>
  );
}
```

## src/components/StepSeparator.tsx
```
// src/components/StepSeparator.tsx
import React from 'react';
import { LightBulbIcon, ChatBubbleLeftRightIcon, PuzzlePieceIcon } from '@heroicons/react/24/outline';
import { BrainIcon } from 'lucide-react';

export function StepSeparator() {
    return (
      <div className="relative py-8">
        <div className="absolute inset-0 flex items-center justify-center" aria-hidden="true">
          <div className="h-full w-[2px] bg-gray-300"></div>
        </div>
        <div className="relative flex justify-center items-center max-w-5xl mx-auto">
          <div className="flex flex-col items-center">
            <span className="h-8 w-8 rounded-full bg-yellow-500 flex items-center justify-center">
              <LightBulbIcon className="h-4 w-4 stroke-white" />
            </span>
            <span className="text-sm font-semibold text-gray-500 whitespace-nowrap mt-2 text-center">Escolha sua ideia</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
              <BrainIcon className="h-4 w-4 stroke-white" />
            </span>
            <span className="text-sm font-semibold text-gray-500 whitespace-nowrap mt-2 text-center">Gere o Plano de negócio com ajuda da IA</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="h-8 w-8 rounded-full bg-green-500 flex items-center justify-center">
              <ChatBubbleLeftRightIcon className="h-4 w-4 stroke-white" />
            </span>
            <span className="text-sm font-semibold text-gray-500 whitespace-nowrap mt-2 text-center">Tire suas dúvidas com nosso time de especialistas</span>
          </div>
          <div className="flex flex-col items-center">
            <span className="h-8 w-8 rounded-full bg-gray-500 flex items-center justify-center">
              <PuzzlePieceIcon className="h-4 w-4 stroke-white" />
            </span>
            <span className="text-sm font-semibold text-gray-500 whitespace-nowrap mt-2 text-center">Lance seu saas com nossas ferramentas</span>
          </div>
        </div>
      </div>
    );
}
```

## src/components/Footer.tsx
```
// src/components/Footer.tsx
import { useTranslations } from "next-intl";
import Image from "next/image";
import Link from "next/link";
 export function Footer() {
     const t = useTranslations('FooterSection');

    return (
        <footer className="bg-white border-t py-8">
            <div className="container mx-auto flex flex-col md:flex-row justify-between items-center text-center md:text-left">
                <div className="mb-4 md:mb-0">
                  <Link href="/" className="text-xl font-semibold flex items-center">
                        <span className="text-blue-600">Idea</span>Forge
                    </Link>
                    <p className="text-gray-500 text-sm">
                         {t('text1')}
                       </p>
                </div>
                {/* <div className="flex flex-col md:flex-row  md:space-x-16  mb-4 md:mb-0">
                      <div>
                        <h4 className="font-semibold mb-2">About</h4>
                        <ul className="text-gray-500">
                          <li className="mb-1">
                             <Link href="/pricing" className="hover:text-blue-600">Pricing</Link>
                          </li>
                           <li className="mb-1">
                               <Link href="/wall-of-love" className="hover:text-blue-600">Wall of Love</Link>
                            </li>
                        </ul>
                     </div>
                    <div>
                      <h4 className="font-semibold mb-2">Resources</h4>
                        <ul className="text-gray-500">
                          <li className="mb-1">
                              <Link href="/docs" className="hover:text-blue-600">Docs</Link>
                            </li>
                            <li className="mb-1">
                               <Link href="/faq" className="hover:text-blue-600">FAQ</Link>
                             </li>
                        </ul>
                     </div>
                     <div>
                        <h4 className="font-semibold mb-2">Legal</h4>
                        <ul className="text-gray-500">
                          <li className="mb-1">
                             <Link href="/terms-of-service" className="hover:text-blue-600">Terms of Service</Link>
                            </li>
                            <li className="mb-1">
                              <Link href="/privacy-policy" className="hover:text-blue-600">Privacy</Link>
                            </li>
                        </ul>
                     </div>
                 </div> */}
                 <div className="text-center md:text-right">
                        <p className="text-gray-500 text-sm mb-2">{t('text2')}</p>
                       <div className="flex items-center justify-center md:justify-end">
                            <span className="text-blue-600">Idea</span>Forge
                            <p className="text-gray-500 ml-1 text-sm">{t('text3')}</p>
                       </div>
               </div>
            </div>
       </footer>
    );
}
```

## src/components/ValueProposition.tsx
```
// src/components/InfoSection.tsx
import React from 'react';
import { useTranslations } from "next-intl";
import { LightBulbIcon, ChatBubbleLeftRightIcon, PuzzlePieceIcon } from '@heroicons/react/24/outline';
import Image from 'next/image';
import { BrainIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface InfoCardProps {
    title: string;
    description: string;
    icon: React.ReactNode;
    iconBgColor?: string;
}
const InfoCard = ({ title, description, icon, iconBgColor }: InfoCardProps) => {
    return (
         <div className="p-4 rounded-md">
            <div className="flex items-center gap-2 mb-2">
                <span className={cn("rounded-full p-2", iconBgColor)}>{icon}</span>
                <h3 className="text-xl font-semibold text-gray-800">{title}</h3>
            </div>
            <p className="text-gray-600">{description}</p>
         </div>
    );
};

export function ValueProposition() {
  const t = useTranslations('ValuePropositionComponent');

    return (
        <section className="py-16">
             <div className="container mx-auto">
                <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-4 text-gray-800 text-center">
                   {t('features_title_part1')}
                </h2>
                <p className="text-base md:text-lg text-gray-600 mb-8 text-center">
                       {t('features_subtitle')}
                </p>
              <div className="flex flex-col md:flex-row justify-center items-center gap-8">
                <div className="md:w-1/4">
                     <InfoCard
                           title={t('feature_title_1')}
                            description={t('feature_description_1')}
                            icon={<LightBulbIcon className="h-6 w-6 stroke-white" />}
                            iconBgColor='bg-yellow-500'
                       />
                      <InfoCard
                            title={t('feature_title_2')}
                            description={t('feature_description_2')}
                          icon={<BrainIcon className="h-6 w-6 stroke-white" />}
                          iconBgColor='bg-blue-500'
                        />
                </div>
                    <div className="flex items-center justify-center md:w-1/4">
                        <div className="rounded-md  p-2 text-center">
                            {/* <span className="text-4xl font-bold">AI</span> */}
                            <Image
                                src="/ai.svg" // Caminho para a sua imagem
                                alt="Ícone de IA" // Texto alternativo para acessibilidade
                                width={250}     // Largura da imagem
                                height={250}    // Altura da imagem
                                priority
                            />
                        </div>
                     </div>
                    <div className="md:w-1/4">
                          <InfoCard
                              title={t('feature_title_3')}
                                 description={t('feature_description_3')}
                               icon={<ChatBubbleLeftRightIcon className="h-6 w-6 stroke-white" />}
                               iconBgColor='bg-green-500'
                          />
                        <InfoCard
                                title={t('feature_title_4')}
                                 description={t('feature_description_4')}
                                icon={<PuzzlePieceIcon className="h-6 w-6 stroke-white" />}
                                iconBgColor='bg-gray-500'
                           />
                    </div>
                </div>
            </div>
        </section>
    );
}
```

## src/components/TestimonialsSection.tsx
```
// src/components/TestimonialsSection.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { useTranslations } from "next-intl";

export function TestimonialsSection() {
 const t = useTranslations('TestimonialsSection');
    return (
    <section className="py-16">
        <div className="container mx-auto text-center">
          <h2 className="text-5xl font-bold mb-8">{t('title')}</h2>
             <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <Card key="1" className="p-6 border">
                    <CardContent>
                        <p className="text-gray-700 mb-4 italic">"{t('text_1')}"</p>
                            <div className="flex items-center mt-4">
                                    <Avatar>
                                        <AvatarImage src="/user1.jpg" alt="Ana Silva" />
                                        <AvatarFallback>AS</AvatarFallback>
                                    </Avatar>
                                <div className="ml-4 text-left">
                                    <p className="font-semibold">{t('name_1')}</p>
                                    <p className="text-gray-500 text-sm">{t('role_1')}</p>
                                </div>
                            </div>
                    </CardContent>
                </Card>
                <Card key="2" className="p-6 border">
                    <CardContent>
                        <p className="text-gray-700 mb-4 italic">"{t('text_2')}"</p>
                            <div className="flex items-center mt-4">
                                    <Avatar>
                                        <AvatarImage src="/user2.jpg" alt="Ana Silva" />
                                        <AvatarFallback>AS</AvatarFallback>
                                    </Avatar>
                                <div className="ml-4 text-left">
                                    <p className="font-semibold">{t('name_2')}</p>
                                    <p className="text-gray-500 text-sm">{t('role_2')}</p>
                                </div>
                            </div>
                    </CardContent>
                </Card>
                    <Card key="3" className="p-6 border">
                        <CardContent>
                            <p className="text-gray-700 mb-4 italic">"{t('text_3')}"</p>
                                <div className="flex items-center mt-4">
                                        <Avatar>
                                            <AvatarImage src="/user3.jpg" alt="Ana Silva" />
                                            <AvatarFallback>AS</AvatarFallback>
                                        </Avatar>
                                    <div className="ml-4 text-left">
                                        <p className="font-semibold">{t('name_3')}</p>
                                        <p className="text-gray-500 text-sm">{t('role_3')}</p>
                                    </div>
                                </div>
                        </CardContent>
                    </Card>
            </div>
        </div>
    </section>
 );
}
```

## src/components/EmailCaptureForm.tsx
```
import { Button, ButtonProps } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import 'react-phone-number-input/style.css';
import { useLocale, useTranslations } from 'next-intl';
import { cn } from "@/lib/utils";
import { saveWaitlistData } from '@/lib/waitlist-service';
import { ClientPhoneInput } from "./ClientPhoneInput";

interface EmailCaptureFormProps {
  buttonText: string;
  buttonVariant: ButtonProps['variant'];
  buttonSize: ButtonProps['size'];
  className?: string;
}

interface FormState {
    loading: boolean;
    success: boolean | null;
    error: string | null;
    phone: string | undefined;
}

async function handleSubmit(prevState: FormState, formData: FormData): Promise<FormState> {
    const name = formData.get('name') as string;
    const email = formData.get('email') as string;
     const phone = formData.get('phone') as string;


    if (!name || !email) {
      return {
        loading: false,
        success: false,
        error: 'Nome e Email são obrigatórios.',
         phone: undefined,
      };
    }

    try {
        await saveWaitlistData(name, email, phone);
      return {
        loading: false,
        success: true,
        error: null,
        phone: undefined,
      };
    } catch (e:any) {
      return {
        loading: false,
        success: false,
        error: 'Ocorreu um erro ao salvar seus dados, por favor tente novamente.',
         phone: undefined,
      };
    }
}

export function EmailCaptureForm({ buttonText, buttonVariant, buttonSize, className }: EmailCaptureFormProps) {
  const t = useTranslations("EmailCaptureForm"); // Usando o mesmo namespace para manter consistência
  const locale = useLocale();
    const [state, setState] = useState<FormState>({
         loading: false,
         success: null,
         error: null,
         phone: undefined,
    });

  const defaultCountry = locale === 'pt' ? 'BR' : 'US';
  const [open, setOpen] = useState(false);

  const handlePhoneChange = (value: string | undefined) => {
        setState((prevState) => ({...prevState, phone: value}))
    };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size={buttonSize} variant={buttonVariant} className={cn("h-16", className)}>{buttonText}</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t('title')}</DialogTitle>
        </DialogHeader>
         {state.error && <p className="text-red-500 text-sm mb-2">{state.error}</p>}
          <form action={async (formData) => {
                const newState = await handleSubmit(state, formData);
                  setState(newState);
                if(newState.success){
                    setOpen(false)
                 }
                }
           } className="flex flex-col gap-4">
            <Input
                type="text"
                name="name"
                placeholder={t('name')}
                required
                disabled={state.loading || state.success === true}
            />
          <Input
            type="email"
            name="email"
            placeholder={t('email')}
            required
            disabled={state.loading || state.success === true}
           />
            <ClientPhoneInput
                placeholder={t('phone')}
                name="phone"
                defaultCountry={defaultCountry}
                className='h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm'
                 onChange={handlePhoneChange}
           />
          <Button type="submit" disabled={state.loading || state.success === true} className="bg-blue-600">
             {state.loading ? 'Enviando...' : state.success === true ? t('msg') : t('btn')}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

## src/components/WaitlistBenefitsSection.tsx
```
// src/components/WaitlistBenefitsSection.tsx
import { useTranslations } from "next-intl";
import { EmailCaptureForm } from "@/components/EmailCaptureForm";

export function WaitlistBenefitsSection() {
  const t = useTranslations("WaitlistBenefitsSection"); // Usando o mesmo namespace para manter consistência
  const button_text = t('call_to_action')

  return (
    <section className="py-16">
      <div className="container mx-auto text-center">
        <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold mb-8">
          {t('title')}
        </h2>

        <div className="max-w-2xl mx-auto">
          <ul className="list-disc pl-4 text-left text-gray-700">
            <li className="mb-4 text-lg">
              {t('b1')}
            </li>
            <li className="mb-4 text-lg">
              {t('b2')}
            </li>
            <li className="mb-4 text-lg">
              {t('b3')}
            </li>
            <li className="mb-4 text-lg">
              {t('b4')}
            </li>
          </ul>
        </div>

        <div className="mt-8">
          <EmailCaptureForm buttonText={button_text} buttonVariant="default" buttonSize="lg" className="bg-blue-600"/>
        </div>
      </div>
    </section>
  );
}
```

## src/components/Header.tsx
```
// src/components/Header.tsx
import { Link } from "@/i18n/routing";
import Image from "next/image";
import { useTranslations } from "next-intl";
import { EmailCaptureForm } from "./EmailCaptureForm";

export function Header() {

const t = useTranslations('HeaderComponent');

  return (
       <header className="bg-white py-7 border-b relative">
            <Image 
               src="/curve-1.png.webp" 
               alt="Curve Top Right" 
               width={1155}
               height={721} 
               className="absolute top-0 right-0 pointer-events-none z-auto"
               priority 
               />
            <div className="container mx-auto flex justify-between items-center flex-col md:flex-row z-auto">
             <Link href="/" className="text-3xl font-semibold mb-4 md:mb-0">
                   <span className="text-blue-600">Idea</span>Forge
               </Link>
               <EmailCaptureForm buttonText={t('call_to_action')} buttonVariant="default" buttonSize="sm" className="bg-blue-600"/>
          </div>
    </header>
   );
}
```

## src/components/IdeaCard.tsx
```
// src/components/IdeaCard.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useTranslations } from "next-intl";

interface Idea {
    id: number;
    name: string;
    description: string;
      diferenciais: string[];
      features: string[];
     implementacaoScore: string;
       marketViabilidadeScore: string;
     categoria: string;
 }

interface IdeaCardProps {
   idea: Idea;
    onPrevious: () => void;
   onNext: () => void;
    disableNextButton:boolean;
    disablePrevButton:boolean;
}
export function IdeaCard({ idea, onPrevious, onNext, disableNextButton, disablePrevButton }: IdeaCardProps) {
     const t = useTranslations('IdeaCardComponent');

     return (
          <div className="container mx-auto py-8">
               <div className="ml-2 mr-2">
                    
                    <Card className="max-w-2xl mx-auto p-2 border">
                         <CardHeader>
                              <CardTitle className="text-2xl font-bold">{idea.name}</CardTitle>
                              <CardDescription className="text-sm text-gray-500">{idea.categoria}</CardDescription>
                         <div className="flex items-center mt-1 gap-2">
                              <Badge variant="outline" className="text-xs">{t('implementation')}: {idea.implementacaoScore}</Badge>
                              <Badge variant="outline" className="text-xs">{t('viability')}: {idea.marketViabilidadeScore}</Badge>
                         </div>
                         </CardHeader>
                         <CardContent>
                                   <p className="text-gray-700 mb-4">
                                        {idea.description}
                                   </p>
                                   <h4 className="font-semibold mb-2 text-gray-900">{t('differentials')}:</h4>
                                   <ul className="list-disc pl-4 mb-4">
                                        {idea.diferenciais.map((diferencial, index) => (
                                             <li key={index} className="text-gray-700 text-sm">
                                                  {diferencial}
                                                  </li>
                                             ))}
                                   </ul>
                                   <h4 className="font-semibold mb-2 text-gray-900">{t('features')}:</h4>
                                   <ul className="list-disc pl-4 mb-4">
                                        {idea.features.map((feature, index) => (
                                             <li key={index} className="text-gray-700 text-sm">
                                                  {feature}
                                             </li>
                                             ))}
                                   </ul>
                              <div className="flex justify-between items-center mt-4 border-t pt-4">
                                   <div className="flex items-center gap-2">
                                        <Button variant="outline" size="icon" disabled={disablePrevButton} onClick={onPrevious}>
                                             <ArrowLeft className="h-4 w-4"/>
                                        </Button>
                              </div>
                                   <div className="flex items-center gap-2">
                                        <Button variant="outline" size="icon" disabled={disableNextButton} onClick={onNext}>
                                        <ArrowRight className="h-4 w-4"/>
                                   </Button>
                                   </div>
                              </div>
                         </CardContent>
                    </Card>
               </div>
          </div>
    );
}
```

## src/components/faq.tsx
```
import React from "react";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/react";
import { ChevronUpIcon } from "@heroicons/react/24/outline";
import Image from "next/image";
import { useTranslations } from "next-intl";

export function Faq() {
    const t = useTranslations('faqSection');
  return (
      <div className="w-full max-w-3xl p-2 mx-auto rounded-2xl">
          <div className="container mx-auto">
                <h2 className="text-2xl md:text-3xl lg:text-5xl font-bold mb-4 text-center">
                    {t('title')}
                </h2>
                <p className="text-base md:text-lg text-gray-500 mb-4 md:mb-8 text-center">
                    {t('sub-title')} <br /> 
                    <span className="text-blue-500">
                          <a href="https://api.whatsapp.com/send?phone=5534988542408&text=I%20am%20interested%20in%20IdeaForge%20DB%20and%20would%20like%20to%20ask%20some%20questions." target="_blank">
                              WhatsApp
                          </a>
                    </span>
                </p>
        </div>
        {/* {faqdata.map((item, index) => ( */}
          <div key={t('q1')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q1')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r1')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>

          <div key={t('q2')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q2')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r2')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>

          <div key={t('q3')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q3')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r3')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>

          <div key={t('q4')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q4')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r4')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>

          <div key={t('q5')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q5')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r5')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>

          <div key={t('q6')} className="mb-5">
            <Disclosure as="div">
              {({ open }) => (
                <>
                  <DisclosureButton  as="div" className="flex items-center justify-between w-full px-4 py-4 text-lg text-left text-gray-800 rounded-lg bg-gray-50 hover:bg-gray-100 focus:outline-none focus-visible:ring focus-visible:ring-indigo-100 focus-visible:ring-opacity-75 dark:bg-trueGray-800 dark:text-gray-200">
                    <span>{t('q6')}</span>
                    <ChevronUpIcon
                      className={`${
                        open ? "transform rotate-180" : ""
                      } w-5 h-5 text-indigo-500`}
                    />
                  </DisclosureButton>
                  <DisclosurePanel as="div" className="px-4 pt-4 pb-2 text-gray-500 dark:text-gray-300">
                  {t('r6')}
                  </DisclosurePanel>
                </>
              )}
            </Disclosure>
          </div>
        {/* ))} */}
        <br /><br />
      </div>
      
  );
}

const faqdata = [
  {
    question: "Is this template completely free to use?",
    answer: "Yes, this template is completely free to use.",
  },
  {
    question: "Can I use it in a commercial project?",
    answer: "Yes, this you can.",
  },
  {
    question: "What is your refund policy? ",
    answer:
      "If you're unhappy with your purchase for any reason, email us within 90 days and we'll refund you in full, no questions asked.",
  },
  {
    question: "Do you offer technical support? ",
    answer:
      "No, we don't offer technical support for free downloads. Please purchase a support plan to get 6 months of support.",
  },
];
```

## src/components/FeaturesSection.tsx
```
// src/components/FeaturesSection.tsx
  import { useTranslations } from "next-intl";
  import { Badge } from "@/components/ui/badge";
  import { RocketLaunchIcon } from "@heroicons/react/24/outline";
  import { Alert } from "@/components/ui/alert";
 import { Card, CardContent } from "@/components/ui/card";
  import { BoltIcon, KeyIcon, ViewColumnsIcon } from "@heroicons/react/24/outline";
  import Image from 'next/image';

 export function FeaturesSection() {
       const t = useTranslations('FeaturesComponent');
     return (
         <section className="py-16 relative">
            <Image
                src="/curve-2.png.webp"
                alt="Curve Left"
                width={414}
                height={825}
                className="absolute top-0 left-0 z-0 pointer-events-none"
                priority
                />
             <div className="container mx-auto text-center">
                   <Alert className="mx-auto flex items-center justify-center w-fit mb-8">
                        <div className="flex items-center gap-2">
                             <RocketLaunchIcon className="w-4 h-4 stroke-blue-700" />
                             <span className="font-semibold">{t('all_in_one')} <br /></span>
                         </div>
                    </Alert>
                    <h2 className="text-2xl md:text-3xl lg:text-5xl font-bold mb-4">
                        {t('features_title_part1')} <br /> {t('features_title_part2')}
                    </h2>
                    <p className="text-base md:text-lg text-gray-500 mb-4 md:mb-8 text-center">
                        {t('features_subtitle')}
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                         <Card className="border ml-2 mr-2 z-10">
                              <CardContent className="flex flex-col items-center p-6 bg-white">
                                   <BoltIcon className="w-8 h-8 mb-2 stroke-blue-500"/>
                                     <h3 className="text-xl font-semibold mb-2">{t('feature_title_1')}</h3>
                                    <p className="text-gray-700 text-sm">
                                       {t('feature_description_2')}
                                     </p>
                              </CardContent>
                          </Card>
                          <Card className="border ml-2 mr-2 z-10">
                               <CardContent className="flex flex-col items-center p-6">
                                   <KeyIcon className="w-8 h-8 mb-2 stroke-blue-500"/>
                                     <h3 className="text-xl font-semibold mb-2">{t('feature_title_2')}</h3>
                                      <p className="text-gray-700 text-sm">
                                          {t('feature_description_2')}
                                       </p>
                              </CardContent>
                         </Card>
                         <Card className="border ml-2 mr-2 z-10">
                             <CardContent className="flex flex-col items-center p-6">
                                  <ViewColumnsIcon className="w-8 h-8 mb-2 stroke-blue-500"/>
                                   <h3 className="text-xl font-semibold mb-2">{t('feature_title_3')}</h3>
                                   <p className="text-gray-700 text-sm">
                                       {t('feature_description_3')}
                                   </p>
                              </CardContent>
                          </Card>
                      </div>
                 </div>
            </section>
         );
 }
```

## src/components/DiscountSection.tsx
```
// src/components/Hero.tsx
import { useTranslations } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Alert } from "@/components/ui/alert";
import { GiftIcon } from "@heroicons/react/24/outline"

export function DiscountSection() {
    const t = useTranslations('HeroComponent');

    return (
        <div className="flex items-center justify-center space-x-4 mb-8 ml-2 mr-2">
            <Alert className="flex items-center space-x-4 w-fit mx-auto px-4">
            <div className="flex items-center gap-2">
                <GiftIcon className="w-4 h-4 stroke-blue-700" />
                <span className="font-semibold text-sm text-center">{t('hero_discount')}</span>
            </div>
            <Badge variant="destructive" className="text-xs text-center">{t('hero_remaining')}</Badge>
            </Alert>
        </div>
    );
}
```

## src/components/ui/card.tsx
```
import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-xl border bg-card text-card-foreground shadow",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("font-semibold leading-none tracking-tight", className)}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

```

## src/components/ui/accordion.tsx
```
"use client"

import * as React from "react"
import * as AccordionPrimitive from "@radix-ui/react-accordion"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

const Accordion = AccordionPrimitive.Root

const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item
    ref={ref}
    className={cn("border-b", className)}
    {...props}
  />
))
AccordionItem.displayName = "AccordionItem"

const AccordionTrigger = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 text-sm font-medium transition-all hover:underline text-left [&[data-state=open]>svg]:rotate-180",
        className
      )}
      {...props}
    >
      {children}
      <ChevronDown className="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
))
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName

const AccordionContent = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className="overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    {...props}
  >
    <div className={cn("pb-4 pt-0", className)}>{children}</div>
  </AccordionPrimitive.Content>
))
AccordionContent.displayName = AccordionPrimitive.Content.displayName

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }

```

## src/components/ui/alert.tsx
```
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const alertVariants = cva(
  "relative w-full rounded-lg border px-4 py-3 text-sm [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground [&>svg~*]:pl-7",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive:
          "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & VariantProps<typeof alertVariants>
>(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props}
  />
))
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-medium leading-none tracking-tight", className)}
    {...props}
  />
))
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm [&_p]:leading-relaxed", className)}
    {...props}
  />
))
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }

```

## src/components/ui/avatar.tsx
```
"use client"

import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"

import { cn } from "@/lib/utils"

const Avatar = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn(
      "relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full",
      className
    )}
    {...props}
  />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Image>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props}
  />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef<
  React.ElementRef<typeof AvatarPrimitive.Fallback>,
  React.ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>
>(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-muted",
      className
    )}
    {...props}
  />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }

```

## src/components/ui/menubar.tsx
```
"use client"

import * as React from "react"
import * as MenubarPrimitive from "@radix-ui/react-menubar"
import { Check, ChevronRight, Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const MenubarMenu = MenubarPrimitive.Menu

const MenubarGroup = MenubarPrimitive.Group

const MenubarPortal = MenubarPrimitive.Portal

const MenubarSub = MenubarPrimitive.Sub

const MenubarRadioGroup = MenubarPrimitive.RadioGroup

const Menubar = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Root>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Root>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Root
    ref={ref}
    className={cn(
      "flex h-9 items-center space-x-1 rounded-md border bg-background p-1 shadow-sm",
      className
    )}
    {...props}
  />
))
Menubar.displayName = MenubarPrimitive.Root.displayName

const MenubarTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-3 py-1 text-sm font-medium outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      className
    )}
    {...props}
  />
))
MenubarTrigger.displayName = MenubarPrimitive.Trigger.displayName

const MenubarSubTrigger = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubTrigger>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubTrigger> & {
    inset?: boolean
  }
>(({ className, inset, children, ...props }, ref) => (
  <MenubarPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      inset && "pl-8",
      className
    )}
    {...props}
  >
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </MenubarPrimitive.SubTrigger>
))
MenubarSubTrigger.displayName = MenubarPrimitive.SubTrigger.displayName

const MenubarSubContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.SubContent>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.SubContent>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
      className
    )}
    {...props}
  />
))
MenubarSubContent.displayName = MenubarPrimitive.SubContent.displayName

const MenubarContent = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Content>
>(
  (
    { className, align = "start", alignOffset = -4, sideOffset = 8, ...props },
    ref
  ) => (
    <MenubarPrimitive.Portal>
      <MenubarPrimitive.Content
        ref={ref}
        align={align}
        alignOffset={alignOffset}
        sideOffset={sideOffset}
        className={cn(
          "z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
          className
        )}
        {...props}
      />
    </MenubarPrimitive.Portal>
  )
)
MenubarContent.displayName = MenubarPrimitive.Content.displayName

const MenubarItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Item> & {
    inset?: boolean
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      inset && "pl-8",
      className
    )}
    {...props}
  />
))
MenubarItem.displayName = MenubarPrimitive.Item.displayName

const MenubarCheckboxItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.CheckboxItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.CheckboxItem>
>(({ className, children, checked, ...props }, ref) => (
  <MenubarPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    checked={checked}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.CheckboxItem>
))
MenubarCheckboxItem.displayName = MenubarPrimitive.CheckboxItem.displayName

const MenubarRadioItem = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.RadioItem>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.RadioItem>
>(({ className, children, ...props }, ref) => (
  <MenubarPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  >
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Circle className="h-4 w-4 fill-current" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.RadioItem>
))
MenubarRadioItem.displayName = MenubarPrimitive.RadioItem.displayName

const MenubarLabel = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Label> & {
    inset?: boolean
  }
>(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Label
    ref={ref}
    className={cn(
      "px-2 py-1.5 text-sm font-semibold",
      inset && "pl-8",
      className
    )}
    {...props}
  />
))
MenubarLabel.displayName = MenubarPrimitive.Label.displayName

const MenubarSeparator = React.forwardRef<
  React.ElementRef<typeof MenubarPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof MenubarPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <MenubarPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props}
  />
))
MenubarSeparator.displayName = MenubarPrimitive.Separator.displayName

const MenubarShortcut = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLSpanElement>) => {
  return (
    <span
      className={cn(
        "ml-auto text-xs tracking-widest text-muted-foreground",
        className
      )}
      {...props}
    />
  )
}
MenubarShortcut.displayname = "MenubarShortcut"

export {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
  MenubarSeparator,
  MenubarLabel,
  MenubarCheckboxItem,
  MenubarRadioGroup,
  MenubarRadioItem,
  MenubarPortal,
  MenubarSubContent,
  MenubarSubTrigger,
  MenubarGroup,
  MenubarSub,
  MenubarShortcut,
}

```

## src/components/ui/dialog.tsx
```
"use client"

import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root

const DialogTrigger = DialogPrimitive.Trigger

const DialogPortal = DialogPrimitive.Portal

const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col space-y-1.5 text-center sm:text-left",
      className
    )}
    {...props}
  />
)
DialogHeader.displayName = "DialogHeader"

const DialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      "flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2",
      className
    )}
    {...props}
  />
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      "text-lg font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
DialogDescription.displayName = DialogPrimitive.Description.displayName

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogTrigger,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}

```

## src/components/ui/badge.tsx
```
import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }

```

## src/components/ui/button.tsx
```
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline:
          "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }

```

## src/components/ui/select.tsx
```
"use client"

import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { Check, ChevronDown, ChevronUp } from "lucide-react"

import { cn } from "@/lib/utils"

const Select = SelectPrimitive.Root

const SelectGroup = SelectPrimitive.Group

const SelectValue = SelectPrimitive.Value

const SelectTrigger = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Trigger>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
      className
    )}
    {...props}
  >
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
))
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName

const SelectScrollUpButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollUpButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollUpButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
))
SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName

const SelectScrollDownButton = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.ScrollDownButton>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.ScrollDownButton>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn(
      "flex cursor-default items-center justify-center py-1",
      className
    )}
    {...props}
  >
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
))
SelectScrollDownButton.displayName =
  SelectPrimitive.ScrollDownButton.displayName

const SelectContent = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Content>
>(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 max-h-96 min-w-[8rem] overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
        className
      )}
      position={position}
      {...props}
    >
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn(
          "p-1",
          position === "popper" &&
            "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]"
        )}
      >
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
))
SelectContent.displayName = SelectPrimitive.Content.displayName

const SelectLabel = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Label>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", className)}
    {...props}
  />
))
SelectLabel.displayName = SelectPrimitive.Label.displayName

const SelectItem = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Item>
>(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  >
    <span className="absolute right-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>
    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
))
SelectItem.displayName = SelectPrimitive.Item.displayName

const SelectSeparator = React.forwardRef<
  React.ElementRef<typeof SelectPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof SelectPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props}
  />
))
SelectSeparator.displayName = SelectPrimitive.Separator.displayName

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
}

```

## src/components/ui/input.tsx
```
import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }

```

## src/components/simple-icons/WhatsappIcon.tsx
```
// src/components/icons/WhatsappIcon.tsx
import * as React from 'react';

interface WhatsappIconProps extends React.SVGProps<SVGSVGElement> {
     size?: string | number;
}

export function WhatsappIcon({ size = 24, ...props }: WhatsappIconProps) {
    return (
        <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
         width={size}
        height={size}
          {...props}
    >
        <path
        fillRule="evenodd"
        d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75 0 2.348.834 4.58 2.25 6.226l-1.602 2.74a.75.75 0 00.707 1.035l2.372-.676c1.72.88 3.717 1.373 5.723 1.373 5.385 0 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm4.5 10.5a.75.75 0 01-.75.75h-2.25a.75.75 0 01-.75-.75v-2.25a.75.75 0 01.75-.75h2.25a.75.75 0 01.75.75v2.25zm-7.5 0a.75.75 0 01-.75.75H8.25a.75.75 0 01-.75-.75v-2.25a.75.75 0 01.75-.75H10.5a.75.75 0 01.75.75v2.25zM15 7a1 1 0 11-2 0 1 1 0 012 0zM9 7a1 1 0 11-2 0 1 1 0 012 0z"
        clipRule="evenodd"
        />
    </svg>
    );
}
```

## src/lib/newsletter-service.ts
```typescript
// src/lib/newsletter-service.ts
import { db } from '@/lib/firebase';
import { collection, addDoc } from 'firebase/firestore';

export async function saveNewsletterEmail(email: string) {
  try {
    const docRef = await addDoc(collection(db, "newsletter"), {
      email,
      createdAt: new Date(),
    });
    console.log("Newsletter email saved with ID:", docRef.id);
  } catch (error) {
      console.error("Error saving newsletter email:", error);
      throw new Error("Failed to save newsletter email.");
  }
}
```

## src/lib/firebase.ts
```typescript
// src/lib/firebase.ts
import { initializeApp, getApps, FirebaseApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
    authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
    projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
    storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};


let firebaseApp: FirebaseApp;

if (!getApps().length) {
    firebaseApp = initializeApp(firebaseConfig)
}else{
    firebaseApp = getApps()[0];
}

const db = getFirestore(firebaseApp)


export { db, firebaseApp };
```

## src/lib/utils.ts
```typescript
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

```

## src/lib/waitlist-service.ts
```typescript
// src/lib/waitlist-service.ts
import { db } from '@/lib/firebase';
import { collection, addDoc } from 'firebase/firestore';

export async function saveWaitlistData(name: string, email: string, phone: string) {
  try {
    const docRef = await addDoc(collection(db, "waitlist"), {
      name,
      email,
      phone: phone || "", // Use string vazia caso o telefone seja undefined
      createdAt: new Date()
    });
    console.log("Waitlist data saved with ID:", docRef.id);
    return docRef.id;
  } catch (error) {
      console.error("Error saving waitlist data:", error);
      throw new Error("Failed to save waitlist data.");
  }
}
```

## src/i18n/routing.ts
```typescript
import {defineRouting} from 'next-intl/routing';
import {createNavigation} from 'next-intl/navigation';

export const routing = defineRouting({
 locales: ['en', 'pt'],
 defaultLocale: 'en',
 pathnames: {
    "/": {
      en: "/",
      pt: "/",
    },
  },
});

export const {Link, redirect, usePathname, useRouter, getPathname} = createNavigation(routing);
```

## src/i18n/request.ts
```typescript
import {getRequestConfig} from 'next-intl/server';
import {routing} from './routing';
 
export default getRequestConfig(async ({requestLocale}) => {
  // This typically corresponds to the `[locale]` segment
  let locale = await requestLocale;
 
  // Ensure that a valid locale is used
  if (!locale || !routing.locales.includes(locale as any)) {
    locale = routing.defaultLocale;
  }
 
  return {
    locale,
    messages: (await import(`../../messages/${locale}.json`)).default
  };
});
```

