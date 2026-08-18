# ADR-0015: LiveKit and SIP Telephony Strategy Decision

**Project:** Voice Agent SaaS Platform  
**Document:** LiveKit + SIP Telephony Architecture Strategy  
**ADR Number:** ADR-0015  
**Version:** 2.0  
**Status:** Accepted  
**Date:** 2026-07-24


---

# 1. Decision Summary

The Voice Agent SaaS Platform will use LiveKit as the real-time media infrastructure and SIP-based telephony integration for production voice communication.

The approved architecture:


| Capability | Decision |
|---|---|
| Telephony provider | Twilio SIP |
| SIP connectivity | SIP Trunking |
| Real-time media server | LiveKit |
| Voice session layer | LiveKit Rooms |
| Agent connection | LiveKit Agents Framework |
| Media transport | WebRTC / RTP |
| Call control | SIP APIs + application logic |
| Recording | LiveKit recording pipeline |
| Scaling model | Distributed voice workers |


This decision creates a flexible voice platform while avoiding dependence on a single AI voice vendor.

---

# 2. Context


The platform requires enterprise voice capabilities:



Customer Phone Call

    |

PSTN Network

    |

Telephony Provider

    |

AI Voice Agent

    |

Business Workflow



The system must support:


- Inbound calls
- Outbound campaigns
- Multiple phone numbers
- Multiple tenants
- Real-time AI conversations
- Call recording
- Human transfers


---

# 3. Problem Statement


A voice AI platform requires several capabilities:


## Telephony Connectivity


Need support for:


- Phone numbers
- PSTN connectivity
- SIP routing


---

## Real-Time Audio Processing


Need:


- Low latency audio streaming
- Media management
- Session handling


---

## AI Integration


Need:


- STT
- LLM
- TTS
- Agent workflows


---

## Scalability


Need support for:


- Thousands of concurrent calls
- Independent worker scaling


---

# 4. Architecture Goals


The selected architecture must provide:


## Provider Independence


The platform should replace:



Telephony Provider

STT Provider

TTS Provider

LLM Provider



without rewriting the entire system.


---

## Real-Time Performance


Voice conversations require:


- Low latency
- Streaming responses
- Stable connections


---

## Enterprise Capability


Support:


- SIP trunks
- Business phone systems
- Call routing


---

# 5. Options Considered


---

# Option 1: Build Custom Media Server


Architecture:



SIP

|

Custom RTP Server

|

AI Pipeline



## Advantages


- Full control


## Disadvantages


- Extremely complex
- High maintenance
- Difficult scaling


## Decision

Rejected.


---

# Option 2: Use Telephony Provider Voice APIs Only


Architecture:



Phone Network

|

Telephony Voice API

|

AI Application



## Advantages


- Fast development
- Simple integration


## Disadvantages


- Vendor lock-in
- Limited media control
- Less flexibility


## Decision

Rejected as primary architecture.


---

# Option 3: SIP + LiveKit Architecture


Architecture:



PSTN

|

SIP Provider

|

LiveKit

|

AI Runtime



## Advantages


- Real-time media control
- Scalable
- Open architecture
- AI friendly


## Decision

Accepted.


---

# 6. Final Architecture


                 Customer


                    |


                Phone Call


                    |


                   PSTN


                    |


              Twilio SIP


                    |


              SIP Gateway


                    |


               LiveKit Room


                    |


          -------------------


          |                 |


    Voice Worker       Recording


          |


          v


      AI Runtime


          |


   STT → LLM → TTS


---

# 7. LiveKit Role


LiveKit is responsible for:


## Media Transport


Handles:


- Audio streams
- Real-time communication
- Participant connections


---

## Room Management


Each call maps to:



LiveKit Room



Example:



room:

tenant123-call456



---

## Participant Management


Participants:



Customer

AI Agent

Human Agent



---

# 8. SIP Integration Strategy


The SIP layer provides:


## Incoming Calls


Flow:



Phone Number

  |

Twilio SIP

  |

LiveKit SIP Gateway

  |

Agent Worker



---

## Outgoing Calls


Flow:



Campaign

  |

Dial Request

  |

Twilio

  |

SIP Connection

  |

LiveKit Agent



---

# 9. Phone Number Management


Phone numbers belong to tenants.


Example:



Tenant A

|

+1-555-0001

Tenant B

|

+1-555-0002



The system stores:



phone_number

tenant_id

assigned_agent_id

provider_configuration



---

# 10. Call Session Model


Each active call contains:



Call ID

Tenant ID

Room ID

Agent ID

Caller Number

Destination Number

Status

Start Time

End Time



---

# 11. Voice Worker Architecture


Workers are responsible for:


- Joining LiveKit rooms
- Running AI agents
- Processing audio
- Executing workflows


Architecture:



LiveKit Room

  |

Voice Worker

  |

AI Runtime

  |

Agent Workflow



---

# 12. Agent Dispatch Strategy


Calls are routed:



Incoming Call

  |

Phone Number Lookup

  |

Tenant Lookup

  |

Agent Selection

  |

Worker Dispatch



---

# 13. Recording Strategy


The system supports:


- Full call recording
- Audio storage
- Transcript generation


Storage:



Object Storage

  |

Tenant Folder

  |

Recording File



---

# 14. Human Transfer Strategy


Transfer flow:



AI Agent

  |

Transfer Decision

  |

SIP Transfer

  |

Human Phone / Agent



---

# 15. Failure Handling


The system handles:


## SIP Failure


Actions:

- Retry
- Failover
- Logging


---

## Worker Failure


Actions:

- Reassign session
- Record failure
- Notify monitoring


---

## Provider Failure


Actions:

- Provider fallback
- Alert operations


---

# 16. Security Requirements


Protect:


- SIP credentials
- Phone numbers
- Call recordings
- Transcripts


Controls:


- Encryption
- Secret management
- Tenant validation
- Access policies


---

# 17. Observability Requirements


Track:


## Call Metrics


- Duration
- Connection status
- Quality


---

## Media Metrics


- Audio latency
- Packet loss
- Disconnects


---

## AI Metrics


- Response latency
- Tool calls
- Completion


---

# 18. Scaling Strategy


Components scale independently.


## LiveKit


Scale by:


- CPU
- Rooms
- Participants


---

## Voice Workers


Scale by:


- Active calls
- Queue depth


---

## AI Runtime


Scale by:


- Agent executions
- Model latency


---

# 19. Implementation Rules


## Rule 1

Every call requires tenant identification.


---

## Rule 2

Every call lifecycle change creates events.


---

## Rule 3

Phone numbers belong to tenants.


---

## Rule 4

Voice providers must remain replaceable.


---

## Rule 5

Recordings require authorization.


---

# 20. Consequences


## Positive Consequences


- Enterprise SIP support
- Flexible AI integration
- Real-time performance
- Scalable voice infrastructure


---

## Negative Consequences


- Additional infrastructure complexity
- Requires real-time engineering expertise
- More operational monitoring


---

# 21. Future Evolution


Future capabilities:


- Multiple SIP providers
- Regional media servers
- Advanced call routing
- Voice quality optimization
- AI voice analytics


Major architectural changes require new ADRs.


---

# 22. Related Documents


Architecture:


- 09_Voice_Call_Flow.md
- 10_AI_Runtime_Architecture.md
- 15_Deployment_Architecture.md


Related ADRs:


- ADR-0014_Voice_Platform_Strategy.md
- ADR-0005_AI_Runtime_Architecture.md


---

# Final Statement


The Voice Agent SaaS Platform will use LiveKit as the real-time communication layer combined with SIP telephony infrastructure.

This architecture provides:

- Production voice capability
- Real-time AI conversations
- SIP compatibility
- Multi-tenant scalability
- Future provider flexibility