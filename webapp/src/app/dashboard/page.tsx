import Image from 'next/image'


export default function Dashboard() {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
            <Image src="/assets/logo.svg" alt="Steering Wheel" width={600} height={600} />
      </div>
    );
  }
  