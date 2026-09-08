import { CampusEvent } from '../types';

export const MOCK_EVENTS: CampusEvent[] = [
  {
    id: 1,
    title: "Autonomous Agents Hackathon 2026",
    description: "48-hour build sprint dedicated to multi-agent coding assistants, LLM tools, and self-hosted infrastructure. Bring your team, pitch before industry judges, and win grant prizes.",
    category: "Technical",
    venue: "Turing Innovation Hall 301",
    dateTime: "2026-09-15T09:00:00",
    endDateTime: "2026-09-17T18:00:00",
    maxCapacity: 120,
    registeredCount: 88,
    registrationLink: "https://campusconnect.edu/register/1",
    imageUrl: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80",
    isRecommended: true,
    recommendationReasons: ["Matches your CS major", "High peer engagement"]
  },
  {
    id: 2,
    title: "Inter-Collegiate Symphony & Jazz Gala",
    description: "An evening featuring collegiate orchestral compositions, guest soloists, and modern brass ensembles under the campus amphitheater stars.",
    category: "Cultural",
    venue: "Grand Open-Air Amphitheater",
    dateTime: "2026-09-18T18:30:00",
    endDateTime: "2026-09-18T22:00:00",
    maxCapacity: 350,
    registeredCount: 290,
    registrationLink: "https://campusconnect.edu/register/2",
    imageUrl: "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=800&q=80",
    isRecommended: false
  },
  {
    id: 3,
    title: "Varsity Basketball Championship Finals",
    description: "Cheer on our university team in the national cup finals against State Tech. Free fan jerseys for the first 100 students at courtside.",
    category: "Sports",
    venue: "Main Campus Arena",
    dateTime: "2026-09-20T17:00:00",
    endDateTime: "2026-09-20T20:30:00",
    maxCapacity: 500,
    registeredCount: 460,
    imageUrl: "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80",
    isRecommended: true,
    recommendationReasons: ["Campus spirit event", "Free merchandise included"]
  },
  {
    id: 4,
    title: "Cloud Infrastructure & Kubernetes Hands-on",
    description: "Practical cluster deployment session using Terraform, Docker, and k8s namespaces. Requires laptop with Docker installed.",
    category: "Workshop",
    venue: "Computing Lab 4B",
    dateTime: "2026-09-22T14:00:00",
    endDateTime: "2026-09-22T17:00:00",
    maxCapacity: 45,
    registeredCount: 42,
    registrationLink: "https://campusconnect.edu/register/4",
    imageUrl: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?auto=format&fit=crop&w=800&q=80",
    isRecommended: true,
    recommendationReasons: ["Hands-on lab", "Limited seats (3 left)"]
  },
  {
    id: 5,
    title: "AI Ethics, Governance & Safety Seminar",
    description: "Distinguished guest keynote on policy, algorithmic accountability, and EU AI Act compliance in enterprise deployments.",
    category: "Seminar",
    venue: "Auditorium Hall B",
    dateTime: "2026-09-25T11:00:00",
    endDateTime: "2026-09-25T13:00:00",
    maxCapacity: 200,
    registeredCount: 135,
    registrationLink: "https://campusconnect.edu/register/5",
    imageUrl: "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=800&q=80",
    isRecommended: false
  },
  {
    id: 6,
    title: "Campus Photography & Visual Arts Showcase",
    description: "Student gallery exhibition showcasing architectural photography, digital matte paintings, and short-film trailers produced this semester.",
    category: "Cultural",
    venue: "Fine Arts Gallery & Terrace",
    dateTime: "2026-09-28T10:00:00",
    endDateTime: "2026-09-28T19:00:00",
    maxCapacity: 150,
    registeredCount: 65,
    imageUrl: "https://images.unsplash.com/photo-1452587925148-ce544e77e70d?auto=format&fit=crop&w=800&q=80",
    isRecommended: false
  }
];
