import * as React from 'react';

interface PlayerNameLinkProps {
  name: string;
  base: string;
}
export default function PlayerNameLink(props: PlayerNameLinkProps): JSX.Element {
  const { name, base } = props;
  return (
    <a className='playerNameLink' href={base + "player/" + name}>
      {name}
    </a>
  );
}
